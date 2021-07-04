import datetime
from urllib import request

from django.db import models
from django.utils import timezone

from bs4 import BeautifulSoup


# Create your models here.

class Contest(models.Model):
    contest_id = models.IntegerField()
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField(default=timezone.now)


class Student(models.Model):
    grade = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    cf_id = models.CharField(max_length=200)
    cf_rating = models.IntegerField(default=0)
    last_visit = models.DateTimeField(default=timezone.now)
    last_update_time = models.DateTimeField(default=timezone.now)
    contest = models.ManyToManyField('Contest', through='ContestStudent')

    def update(self):
        self.last_update_time = timezone.now()
        self.save()
        soup = BeautifulSoup(
            request.urlopen("http://codeforces.com/contests/with/%s" % self.cf_id, timeout=10).read().decode('utf-8'),
            'lxml')
        table = soup.find('table', class_='tablesorter user-contests-table').find('tbody')
        trs = table.find_all('tr')

        first = True
        for tr in trs:
            td = tr.find_all('td')

            contest_id = int(td[1].find('a')['href'].split('/')[-1].strip())  # id
            contest_name = td[1].get_text().strip()  # name

            contest_time = td[2].find('a').get_text().strip()  # time
            contest_time = datetime.datetime.strptime(contest_time, '%b/%d/%Y %H:%M') + datetime.timedelta(hours=5)
            contest_time = contest_time.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=0)))

            contest = Contest.objects.get_or_create(contest_id=contest_id, name=contest_name, start_time=contest_time)
            contest = contest[0]

            rank = int(td[3].get_text().strip())
            solved = int(td[4].find('a').get_text().strip())
            rating_change = int(td[5].find('span').get_text().strip())
            new_rating = int(td[6].get_text().strip())

            if first:
                first = False
                self.cf_rating = new_rating
                self.last_update_time = timezone.now()
                self.save()

            if len(self.contest.filter(contest_id=contest_id)) == 0:
                ContestStudent(contest=contest,
                               student=self,
                               rank=rank,
                               solved=solved,
                               rating_change=rating_change,
                               new_rating=new_rating).save()

    @property
    def color(self):
        if self.cf_rating < 1200:
            return "grey"
        if self.cf_rating < 1400:
            return "green"
        if self.cf_rating < 1600:
            return "#03A89D"
        if self.cf_rating < 1900:
            return "blue"
        if self.cf_rating < 2100:
            return "#AA00AA"
        if self.cf_rating < 2400:
            return "#FF8C00"
        if self.cf_rating < 4000:
            return "red"

    @property
    def last_five(self):
        res = []
        contests = self.conteststudent_set.all().order_by("-contest__start_time")
        for contest in contests:
            if len(res) == 5:
                break
            res.append(contest.new_rating)

        res.reverse()
        return str(res)

    def __str__(self):
        return str([self.name, self.cf_id, self.cf_rating])


class ContestStudent(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rank = models.IntegerField()
    solved = models.IntegerField()
    rating_change = models.IntegerField()
    new_rating = models.IntegerField()
