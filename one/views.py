import datetime

from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from . import models
from .models import c_candidate, c_jobs


# Create your views here.


def cinput(request):
    if request.method == "POST":
        name = request.POST.get('nameInput')
        age = request.POST.get('ageInput')
        education = request.POST.get('educationInput')
        skills = request.POST.get('skillsInput')
        phone = request.POST.get('phoneInput')
        username = request.POST.get('usernameInput')
        password = request.POST.get('passwordInput')

        if c_candidate.find_one({'username': username}):
            return render(request, 'candidateInput.html', {'error': 'This username is already taken.'})

        hashed_password = make_password(password)
        document = {"name": name, "age": age, "education": education, "skills": skills, "phone": phone,
                    "username": username, "password": hashed_password, "applied_jobs": [], "status": []}
        c_candidate.insert_one(document)
        return redirect('success')
    return render(request, 'candidateInput.html')


def clogin(request):
    if request.method == 'POST':
        # get the form data from request.POST
        username = request.POST.get('username')
        password = request.POST.get('password')

        # query the database for a document with the matching email

        user = c_candidate.find_one({'username': username})

        if user:
            # check if the input password matches the stored hashed password
            hashed_password = user.get('password')
            if check_password(password, hashed_password):
                request.session['username'] = username
                return redirect('cdash')
            else:
                return render(request, 'candidateLogin.html', {'error': 'Invalid email or password.'})
        else:
            return render(request, 'candidateLogin.html', {'error': 'Invalid email or password.'})
    else:
        return render(request, 'candidateLogin.html')


def logins(request):
    return render(request, "logins.html")


def success(request):
    return render(request, 'success.html')


def home(request):
    return render(request, 'home.html')


def cdash(request):
    # Profile Section
    c_details = c_candidate.find_one({"username": request.session.get('username')})

    # Available Jobs Section
    all_jobs = list(c_jobs.find())
    all_jobs.pop(0)

    # Applied Jobs
    cJobs = c_candidate.find_one({"username": request.session.get('username')})["applied_jobs"]
    cStatus = c_candidate.find_one({"username": request.session.get('username')})["status"]
    appliedJobs = [[a, b] for a, b in zip(cJobs, cStatus)]

    # Apply for Jobs
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        candidate_username = request.session.get('username')

        # update the "applied_candidates" array in a document with a specific heading
        value = c_candidate.find_one({"username": candidate_username})["applied_jobs"]

        if value.count(job_id) < 1:
            print("INSERTING")
            c_jobs.update_one({"heading": job_id}, {"$push": {"applied_candidates": candidate_username}})
            c_candidate.update_one({"username": candidate_username},
                                   {"$push": {"applied_jobs": job_id}})
            c_candidate.update_one({"username": candidate_username},
                                   {"$push": {"status": "pending"}})
            return redirect('cdash')
        else:
            print("ERROR")
            dictionary = {'candidate': c_details, 'jobDetails': all_jobs, 'username': request.session.get('username'),
                          'error': "Already applied to this Job", "applied_jobs": appliedJobs}
            return render(request, 'candidateDashboard.html', dictionary)

    dictionary = {'candidate': c_details, 'jobDetails': all_jobs, 'username': request.session.get('username'), "applied_jobs": appliedJobs}
    return render(request, 'candidateDashboard.html', dictionary)


def logout_view(request):
    logout(request)
    return redirect('home')


# ----------------------------------------------------------------------------------------------------------------------
# JOB SECTION


def jinput(request):
    if request.method == "POST":
        heading = request.POST.get('headingInput')
        role = request.POST.get('roleInput')
        exp = request.POST.get('experienceInput')
        skills = request.POST.get('skillsInput')
        phone = request.POST.get('phoneInput')
        salary = request.POST.get('salaryInput')
        location = request.POST.get('locationInput')
        id2 = heading.replace(" ", "")

        if c_jobs.find_one({'id2': id2}):
            return render(request, 'jobInput.html', {'error': 'This username is already taken.'})

        current_date = datetime.date.today()
        formatted_date = current_date.strftime('%d-%m-%Y')

        current_time = datetime.datetime.now()
        am_pm_time = current_time.strftime('%I:%M:%S %p')

        cTime = am_pm_time + " , " + formatted_date

        document = {"heading": heading, "role": role, "exp": exp, "skills": skills, "phone": phone,
                    "salary": salary, "location": location, "applied_candidates": [], "time_posted": cTime, "id2": id2}
        c_jobs.insert_one(document)
        return redirect('jsuccess')
    return render(request, 'jobInput.html')


def jlogin(request):
    if request.method == 'POST':
        # get the form data from request.POST
        username = request.POST.get('username')
        password = request.POST.get('password')

        # query the database for a document with the matching email

        user = c_jobs.find_one({'username': username})

        if user:
            # check if the input password matches the stored hashed password
            p = user.get('password')
            if password == p:
                request.session['username'] = username
                return redirect('jdash')
            else:
                return render(request, 'jobLogin.html', {'error': 'Invalid email or password.'})
        else:
            return render(request, 'jobLogin.html', {'error': 'Invalid email or password.'})
    else:
        return render(request, 'jobLogin.html')


def jdash(request):
    all_jobs = list(c_jobs.find())
    all_jobs.pop(0)
    no_of_jobs_posted = len(all_jobs)

    # DECLINED
    if request.method == 'POST':
        if request.POST.get('dec_c_name') and request.POST.get('dec_j_name'):
            print("Hey Baby !! I'm in decline mode")
            c_id = request.POST.get('dec_c_name')
            j_id = request.POST.get('dec_j_name')

            # OVERWRITE STATUS IN CANDIDATE COLLECTION
            username = c_id
            new_status = 'declined'

            # Find document with matching name
            document = c_candidate.find_one({"username": username})

            # Find index of element in array
            index = document["applied_jobs"].index(j_id)

            array_with_index = 'status.' + str(index)

            c_candidate.update_one(
                {'username': username},
                {'$set': {array_with_index: new_status}}
            )

            # DELETE FROM JOBS APPLIED_CANDIDATE ARRAY
            c_jobs.update_one({'heading': j_id}, {'$pull': {'applied_candidates': c_id}})

            # WHAT WILL YOU RETURN NOW DUMB FUCK
            # BEAUTIFUL SWEETHEART, ITS WORKING FINE
            redirect("jdash")

        if request.POST.get('app_c_name') and request.POST.get('app_j_name'):
            print("Hey Baby !! I'm in approve mode")
            c_id = request.POST.get('app_c_name')
            j_id = request.POST.get('app_j_name')

            # OVERWRITE STATUS IN CANDIDATE COLLECTION
            username = c_id
            new_status = 'approved'

            # Find document with matching name
            document = c_candidate.find_one({"username": username})

            # Find index of element in array
            index = document["applied_jobs"].index(j_id)

            array_with_index = 'status.' + str(index)

            c_candidate.update_one(
                {'username': username},
                {'$set': {array_with_index: new_status}}
            )

            # DELETE FROM JOBS APPLIED_CANDIDATE ARRAY
            c_jobs.update_one({'heading': j_id}, {'$pull': {'applied_candidates': c_id}})
            redirect("jdash")

    dictionary = {"username": request.session.get('username'), "jobs": all_jobs, "total_jobs": no_of_jobs_posted}
    return render(request, "jobDashboard.html", dictionary)


def jsuccess(request):
    return render(request, "jsuccess.html")


def baseresume(request):
    if request.method == 'POST':
        c_user = request.POST.get('c_username')
        request.session['c_name'] = c_user
        candidate = c_candidate.find_one({"username": c_user})
        dictionary = {"candidate": candidate}
        return render(request, "baseResume.html", dictionary)

    c_user = request.session.get('c_name')
    candidate = c_candidate.find_one({"username": c_user})
    dictionary = {"candidate": candidate}
    return render(request, "baseResume.html", dictionary)

