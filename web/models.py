import datetime
import re
from urllib import request

from django.db import models
from django.utils import timezone

# Create your models here.
re_rating = re.compile('<span style="font-weight:bold;" class="user-[^0-9]*([0-9]*)</span>')
re_number = re.compile('[+|-]*[0-9]+')
re_contest_name = re.compile('title="([^"]*)"')

re_contest_id = re.compile('data-contestId="([0-9]*)"')
re_contest_time = re.compile('<span class="format-date" data-locale="en">(.*)</span>')


def update_contest(url):
    contests = request.urlopen(url).read().decode("utf-8")
    contests = contests.split("Contest history")[1]
    contests = contests.split("<tr")
    for item in contests:
        try:
            contest_id = re_contest_id.findall(item)[0]
            print(contest_id)
            contest_time = re_contest_time.findall(item)[0]
            contest_time = datetime.datetime.strptime(contest_time, '%b/%d/%Y %H:%M') + datetime.timedelta(hours=5)
            contest = Contest.objects.get(contest_id=contest_id)
            contest.time = contest_time.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=0)))
            contest.save()
            print(contest_time)
        except:
            pass
    pass


class Student(models.Model):
    classroom = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    cf_id = models.CharField(max_length=200)
    cf_rating = models.IntegerField(default=0)
    last_visit = models.DateTimeField(default=timezone.now)
    last_update_time = models.DateTimeField(default=timezone.now)
    contest = models.ManyToManyField('Contest', through='ContestStudent')

    def update(self):
        self.last_update_time = timezone.now()
        self.save()
        profile = request.urlopen("http://codeforces.com/profile/%s" % self.cf_id).read().decode('utf-8')
        # print(profile)
        self.cf_rating = int(re_rating.findall(profile)[0])
        self.last_update_time = timezone.now()
        self.save()
        contests = request.urlopen("http://codeforces.com/contests/with/%s" % self.cf_id).read().decode('utf-8')
        contests = contests.split('<td>')
        for i in range(1, len(contests) - 7, 7):
            contest_id = re_number.findall(contests[i + 1])[0]
            contest_name = re_contest_name.findall(contests[i + 1])[0]
            contest = Contest.objects.get_or_create(contest_id=contest_id, name=contest_name)
            if contest[1]:
                update_contest("http://codeforces.com/contests")
                update_contest("http://codeforces.com/contests/page/2")
                update_contest("http://codeforces.com/contests/page/3")
                update_contest("http://codeforces.com/contests/page/4")
            contest = contest[0]
            print(contest)
            rank = int(re_number.findall(contests[i + 2].replace(' ', ''))[3])
            solved = int(re_number.findall(contests[i + 3].split("\n")[2].replace(' ', ''))[0])
            print("solved", solved)
            rating_change = int(re_number.findall(contests[i + 4].replace(' ', ''))[0])
            new_rating = int(re_number.findall(contests[i + 5].replace(' ', ''))[0])
            print(self.contest.count())
            if len(self.contest.filter(contest_id=contest_id)) == 0:
                ContestStudent(contest=contest,
                               student=self,
                               rank=rank,
                               solved=solved,
                               rating_change=rating_change,
                               new_rating=new_rating).save()

    @property
    def color(self):
        if (self.cf_rating < 1200): return "grey"
        if (self.cf_rating < 1400): return "green"
        if (self.cf_rating < 1600): return "03A89D"
        if (self.cf_rating < 1900): return "blue"
        if (self.cf_rating < 2100): return "AA00AA"

    @property
    def last_five(self):
        res = list()
        rating = 1500
        x = self.conteststudent_set.all().order_by("contest__time")
        #if(len(x)==0):return "empty"
        for con in x:
            rating += con.rating_change
            #res.append(con.rating_change)
            res.append(rating)
        res = res[::-1]
        while len(res) > 5: res.pop()
        res=res[::-1]
        return str(res)

    def __str__(self):
        return str([self.name, self.cf_id, self.cf_rating])


class Contest(models.Model):
    contest_id = models.IntegerField()
    name = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now)


class ContestStudent(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rank = models.IntegerField()
    solved = models.IntegerField()
    rating_change = models.IntegerField()
    new_rating = models.IntegerField()
