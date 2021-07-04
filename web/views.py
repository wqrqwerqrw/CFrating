from django.shortcuts import render

# Create your views here.

from .models import Student, Contest, ContestStudent


# Create your views here.
def rating(request):
    return render(request, "rating.html", {"students": Student.objects.all().order_by('-cf_rating')})


def contests(request):
    return render(request, "contests.html", {"contests": Contest.objects.all().order_by('-start_time')})


def contest(request, contest_id):
    return render(request, "contest.html",
                  {"conteststudens": ContestStudent.objects.filter(contest__contest_id=contest_id).order_by('rank'),
                   "contest": Contest.objects.get(contest_id=contest_id)})

def student(request, cf_id):
    return render(request, "student.html",
                  {"conteststudents":ContestStudent.objects.filter(student__cf_id=cf_id).order_by('contest__start_time'),
                   "student": Student.objects.get(cf_id=cf_id)})
