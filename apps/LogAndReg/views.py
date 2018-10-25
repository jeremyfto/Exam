from django.shortcuts import render, redirect
import bcrypt
from .models import User, Job
from django.contrib import messages
import datetime
def index(request):
    return render(request, 'index.html')
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create()
        user.First_Name = request.POST['First_Name']
        user.Last_Name = request.POST['Last_Name']
        user.email = request.POST['email']
        user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user.save()
        messages.success(request, "You have successfully added your account")
        request.session['First_Name'] = request.POST['First_Name']
        request.session['ID'] = user.id
        return redirect('/jobs')
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    Account=User.objects.get(email=request.POST['email'])
    request.session['ID'] = Account.id
    request.session['First_Name'] = Account.First_Name
    return redirect('/jobs')
def Dashboard(request):
    if 'ID' not in request.session:
        return redirect("/")
    jobs = Job.objects.all()
    Cjobs = Job.objects.all().filter(Creator = request.session['ID'])
    OwnedJobs = Job.objects.all().filter(OwnedBy = request.session['ID'])
    CompletedJobs = Job.objects.all().filter(Completed = True)
    OwnerlessJobs = Job.objects.all().filter(OwnedBy = None)
    print(request.session['ID'])
    data = {
        "jobs" : jobs,
        "Cjobs" : Cjobs,
        "OwnedJobs" : OwnedJobs,
        "CompletedJobs": CompletedJobs,
        "OwnerlessJobs" : OwnerlessJobs
    }
    return render(request, 'Dashboard.html', data)
def Logout(request):
    request.session.clear()
    return redirect('/')


def new(request):
    return render(request, 'NewJob.html')
def NewJob(request):
    errors = Job.objects.job_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/new')
    else:
        CurUser=User.objects.get(id=request.session['ID'])
        JobCreator = Job.objects.create(Title = request.POST['Job_Title'], Desc = request.POST['Job_Desc'], Location = request.POST['Job_Loc'],Catagory = request.POST['Catagory'] + " " + request.POST['Other'], Completed = False, Creator = CurUser)
        JobCreator.save()
        print(Job.objects.last().Title)
        return redirect('/jobs')

def delete(request, JobID):
    JobID = Job.objects.get(id=JobID)
    JobID.delete()
    return redirect('/jobs')
def view(request, JobID):
    CurJob=Job.objects.get(id=JobID)
    OwnedJobs = Job.objects.all().filter(OwnedBy = request.session['ID'])
    OwnerlessJobs = Job.objects.all().filter(OwnedBy = None)
    context = {
        "job":CurJob,
        "OwnedJobs":OwnedJobs,
        "CurID" : JobID,
        "OwnerlessJobs" : OwnerlessJobs
    }
    return render(request, 'view.html', context)
def editpage(request, JobID):
    CurJob=Job.objects.get(id=JobID)
    context = {
        "job":CurJob,
        "CurID":JobID
    }
    return render(request, 'EditJob.html', context)
def edit(request, JobID):
    errors = Job.objects.job_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/jobs/edit/'+JobID)
    else:
        CurJob = Job.objects.get(id=JobID)
        CurJob.Title = request.POST['Job_Title']
        CurJob.Desc = request.POST['Job_Desc']
        CurJob.Location = request.POST['Job_Loc']
        CurJob.save()
        print(Job.objects.last().Title)
        return redirect('/jobs')
def add(request, JobID):
    CJobID = Job.objects.get(id=JobID)
    CJobID.OwnedBy = request.session['ID']
    CJobID.save()
    return redirect('/jobs')
def giveup(request, JobID):
    CJobID = Job.objects.get(id=JobID)
    CJobID.OwnedBy = None
    CJobID.save()
    return redirect('/jobs')
def Complete(request, JobID):
    CJobID = Job.objects.get(id=JobID)
    CJobID.Completed = True
    CJobID.save()
    return redirect('/jobs')