import datetime

from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.core.files.storage import FileSystemStorage
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from student_management_app.HodViews import get_country_list, get_course_list, get_session_list
from student_management_app.forms import AddStudentForm, addNoticeform
from student_management_system import settings


from student_management_app.EmailBackEnd import EmailBackEnd
from student_management_app.models import Country, Courses, CustomUser, SessionYearModel, State

# connection = mail.get_connection()




def showDemoPage(request):
    return render(request,"demo.html")

def ShowLoginPage(request):
    return render(request,"login_page.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")
            

def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def signup_admin(request):
    return render(request,"signup_admin_page.html")

def do_admin_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=1)
        user.save()
        messages.success(request,"Successfully Created Admin")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request,"Failed to Create Admin")
        return HttpResponseRedirect(reverse("show_login"))


def signup_student(request):
    states = []
    # courses=Courses.objects.all()
    # session_years=SessionYearModel.object.all()
    # countries=Country.objects.all()
    # states=State.objects.all()
    
    form=AddStudentForm(get_course_list,get_session_list,get_country_list,states)
    return render(request,"signup_student_page.html",{"form":form})

def signup_staff(request):
    return render(request,"signup_staff_page.html")

def do_staff_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
        user.staffs.address=address
        user.save()
        messages.success(request,"Successfully Created Staff")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request,"Failed to Create Staff")
        return HttpResponseRedirect(reverse("show_login"))

def change_states(request):
    # breakpoint()
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country=country_id)
    return render(request, 'state_dropdown.html', {'states': states})

def do_signup_student(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    
    else:
        # breakpoint()
        form=AddStudentForm(get_course_list,get_session_list,get_country_list,get_state_list,request.POST,request.FILES)
        # form=AddStudentForm(request.POST,request.FILES)

        
        if form.is_valid():
            email_exists=True if (CustomUser.objects.filter(email=form.cleaned_data["email"]).exists()) else False
            username_exists=True if (CustomUser.objects.filter(username=form.cleaned_data["username"]).exists()) else False
            if not email_exists and not username_exists:                            
                first_name=form.cleaned_data["first_name"]
                last_name=form.cleaned_data["last_name"]
                username=form.cleaned_data["username"]
                email=form.cleaned_data["email"]
                password=form.cleaned_data["password"]
                prn_number=form.cleaned_data["prn_number"]
                father_name=form.cleaned_data["father_name"]
                mother_name=form.cleaned_data["mother_name"]
                alternate_mobile=form.cleaned_data["alternate_mobile"]
                date_of_birth=form.cleaned_data["date_of_birth"]
                
                admission_type=form.cleaned_data["admission_type"]
                admission_status=form.cleaned_data["admission_status"]
                permanent_address=form.cleaned_data["permanent_address"]
                communication_address=form.cleaned_data["communication_address"]
                
                country=form.cleaned_data["country"]
                state=form.cleaned_data["state"]
                mobile=form.cleaned_data["mobile"]
                session_year=form.cleaned_data["session_year"]
                session_joining_month=form.cleaned_data["session_joining_month"]
                final_fees=form.cleaned_data["final_fees"]
                highest_qualification=form.cleaned_data["highest_qualification"]
                other_information=form.cleaned_data["other_information"]
                course=form.cleaned_data["course"]
                gender=form.cleaned_data["gender"]
                currency_type=form.cleaned_data["currency_type"]

                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
                # try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.students.permanent_address=permanent_address
                user.students.communication_address=communication_address

                country_obj=Country.objects.get(id=country)
                user.students.country=country_obj
                state_obj=State.objects.get(id=state)
                user.students.state=state_obj
                course_obj=Courses.objects.get(id=course)
                user.students.course=course_obj

                session_year_obj=SessionYearModel.object.get(id=session_year)
                user.students.session_year=session_year_obj
                user.students.session_joining_month=session_joining_month
                user.students.gender=gender
                user.students.prn_number=prn_number
                user.students.currency_type=currency_type
                user.students.father_name=father_name
                user.students.mother_name=mother_name
                user.students.alternate_mobile=alternate_mobile
                user.students.date_of_birth=date_of_birth
                user.students.admission_type=admission_type
                user.students.admission_status=admission_status
                user.students.mobile=mobile
                user.students.final_fees=final_fees
                user.students.highest_qualification=highest_qualification
                user.students.other_information=other_information
                user.students.profile_pic=profile_pic_url
                user.save()
                messages.success(request,"Successfully Added Student")
                return HttpResponseRedirect(reverse("show_login"))

            else:
                messages.error(request,"Username or Email already exists")
                return HttpResponseRedirect(reverse("signup_student"))
            # except:
            #     messages.error(request,"Failed to Add Student")
            #     return HttpResponseRedirect(reverse("add_student"))
        else:
            # form=AddStudentForm(request=request)
            # form=AddStudentForm(request.POST)
            form=AddStudentForm(get_course_list,get_session_list,get_country_list,get_state_list,request.POST)
            return render(request,"login_page.html",{"form":form})
    
    #except:
     #   messages.error(request, "Failed to Add Student")
      #  return HttpResponseRedirect(reverse("show_login"

# connection.close()

def get_country_list():
    countries = []
    try:
        list_country = Country.objects.all()
        for country in list_country:
            all_country=(country.id,country.name)
            countries.append(all_country)

    except:
        countries = []

    return countries

def get_state_list():
    states = []
    try:
        list_states = State.objects.all()
        for state in list_states:
            all_states=(state.id,state.name)
            states.append(all_states)

    except:
        states = []

    return states
