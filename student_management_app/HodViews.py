import datetime
from typing import Reversible
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.backends import UserModel
from django.core.files.storage import FileSystemStorage
from django.db.models.fields import DateTimeCheckMixin, DateTimeField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from student_management_app import forms
from student_management_app.StudentViews import student_document
from student_management_app.forms import AddCourseForm, AddStudentForm,EditStudentForm,addNoticeform
from django.views.decorators.csrf import csrf_exempt

from student_management_app.models import Attendance, AttendanceReport, CollegeDocument, Country, CustomUser, Links, Notice, SessionYearModel, Staffs, Courses, State, StudentDocument, Students, Subjects


def admin_home(request):
    student_count1=Students.objects.all().count()
    staff_count=Staffs.objects.all().count()
    subject_count=Subjects.objects.all().count()
    course_count=Courses.objects.all().count()
    notice=Notice.objects.all()

    # notice_all=Notice.objects.all()
    course_all=Courses.objects.all()
    course_name_list=[]
    subject_count_list=[]
    student_count_list_in_course=[]
    for course in course_all:
        subjects=Subjects.objects.filter(course=course.id).count()
        students=Students.objects.filter(course=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    # for notice in notice_all:
    #     notices=Notice.objects.all()

    subjects_all=Subjects.objects.all()
    subject_list=[]
    student_count_list_in_subject=[]
    for subject in subjects_all:
        course=Courses.objects.get(id=subject.course.id)
        student_count=Students.objects.filter(course=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    staffs=Staffs.objects.all()
    attendance_present_list_staff=[]
    attendance_absent_list_staff=[]
    staff_name_list=[]
    for staff in staffs:
        subject_ids=Subjects.objects.filter(staff=staff.admin.id)
        attendance=Attendance.objects.filter(subject_id__in=subject_ids).count()
        # leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
        # attendance_absent_list_staff.append(leaves)
        attendance_present_list_staff.append(attendance)
        staff_name_list.append(staff.admin.username)

    students_all=Students.objects.all()
    attendance_present_list_student=[]
    attendance_absent_list_student=[]
    student_name_list=[]
    for student in students_all:
        attendance=AttendanceReport.objects.filter(student_id=student.id,status=True).count()
        absent=AttendanceReport.objects.filter(student_id=student.id,status=False).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(absent)
        student_name_list.append(student.admin.username)


    return render(request,"hod_template/home_content.html",{"student_count":student_count1,"staff_count":staff_count,"subject_count":subject_count,"course_count":course_count,"course_name_list":course_name_list,"subject_count_list":subject_count_list,"student_count_list_in_course":student_count_list_in_course,"student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list,"staff_name_list":staff_name_list,"attendance_present_list_staff":attendance_present_list_staff,"attendance_absent_list_staff":attendance_absent_list_staff,"student_name_list":student_name_list,"attendance_present_list_student":attendance_present_list_student,"attendance_absent_list_student":attendance_absent_list_student,"notice":notice})


# AJAX
def load_states(request):
    # breakpoint()
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country=country_id)
    return render(request, 'hod_template/state_dropdown_list_options.html', {'states': states})

def change_states(request):
    # breakpoint()
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country=country_id)
    return render(request, 'state_dropdown.html', {'states': states})
    # return JsonResponse(list(states.values('id', 'name')), safe=False)


def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))

def delete_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return HttpResponseRedirect(reverse("manage_staff"))
    except:
        messages.error(request, "Failed to Delete Staff.")
        return HttpResponseRedirect(reverse("manage_staff"))

def add_link(request):
    links=Links.objects.all()
    return render(request,"hod_template/add_link_template.html",{"links":links})

def imp_link_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        if request.POST.get('important_urls')=="":
            messages.error(request, "Failed to Add important url!")
            return HttpResponseRedirect("add_link")
        else:
            important_urls=request.POST.get("important_urls")
            important_name=request.POST.get("important_name")
            important_comment=request.POST.get("important_comment")
            

        try:
            
            links=Links(urls=important_urls,comments=important_comment,name=important_name,types=Links.linkType.IMPORTANT_LINKS)
            links.save()
            messages.success(request,"Successfully Added  important Link")
            return HttpResponseRedirect(reverse("add_link"))
        except:
            messages.error(request,"Failed to Add important links")
            return HttpResponseRedirect(reverse("add_link"))

def cls_link_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        if request.POST.get('class_urls')=="":
            messages.error(request, "Failed to Add Class links!")
            return HttpResponseRedirect("add_link")
        else:
            class_urls=request.POST.get("class_urls")
            class_name=request.POST.get("class_name")
            class_comment=request.POST.get("class_comment")

        try:
            links=Links(urls=class_urls,comments=class_comment,name=class_name,types=Links.linkType.CLASS_LINKS)
            links.save()
            messages.success(request,"Successfully Added Links")
            return HttpResponseRedirect(reverse("add_link"))
        except:
            messages.error(request,"Failed to Add links")
            return HttpResponseRedirect(reverse("add_link"))

def delete_link(request, link_id):
    link = Links.objects.get(id=link_id)
    try:
        # breakpoint()
        link.delete()
        messages.success(request, "link Deleted Successfully.")
        return HttpResponseRedirect(reverse("add_link"))
    except:
        messages.error(request, "Failed to Delete link")
        return HttpResponseRedirect(reverse("add_link"))

def student_doc_approve(request,document_id):
    document=StudentDocument.objects.get(id=document_id)
    document.check_marksheet=1
    document.save()
    return HttpResponseRedirect(reverse("hod_document"))

def student_doc_disapprove(request,document_id):
    document=StudentDocument.objects.get(id=document_id)
    document.check_marksheet=2
    document.save()
    return HttpResponseRedirect(reverse("hod_document"))

def add_course(request):
    course_form=AddCourseForm()
    return render(request,"hod_template/add_course_template.html",{"course_form":course_form})



def add_course_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_course')
    else:
        course_form=AddCourseForm(request.POST)

        if course_form.is_valid():
            course_exists=True if (Courses.objects.filter(course_name=course_form.cleaned_data["course_name"]).exists()) else False
            if not course_exists:
                course_name=course_form.cleaned_data["course_name"]
                course_model = Courses(course_name=course_name)
                course_model.save(force_insert=True)
                messages.success(request, "Course Added Successfully!")
                return HttpResponseRedirect(reverse("add_course"))
            else:
                messages.error(request,"Course already exists")
                return HttpResponseRedirect(reverse("add_course"))
        else:
            form=AddCourseForm(request.POST)
            return render(request,"hod_template/add_course_template.html",{"form":form})



        

def delete_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    try:
        course.delete()
        messages.success(request, "Course Deleted Successfully.")
        return HttpResponseRedirect(reverse("manage_course"))
    except:
        messages.error(request, "Failed to Delete Course.")
        return HttpResponseRedirect(reverse("manage_course"))

def add_student(request):
    # form=AddStudentForm()
    


    states = []
    # try:
    #     list_courses = Courses.objects.all()
    #     for course in list_courses:
    #         small_course=(course.id,course.course_name)
    #         courses.append(small_course)

    # except:
    #     courses = []

    
    
    # sessions = []
    # try:
    #     session_list = SessionYearModel.object.all()

    #     for ses in session_list:
    #         small_ses = (ses.id, str(ses.session_start_year)+"   TO  "+str(ses.session_end_year))
    #         sessions.append(small_ses)
    # except:
    #     sessions=[]

    # countries=[]
    # try:
    #     country_list = Country.objects.all()

    #     for country in country_list:
    #         country_name=(country.id,country.name)
    #         countries.append(country_name)
            
    # except:
    #     countries=[]

    form=AddStudentForm(get_course_list,get_session_list,get_country_list,states)
    return render(request,"hod_template/add_student_template.html",{"form":form})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    
    else:
        # breakpoint()
        form=AddStudentForm(get_course_list,get_session_list,get_country_list,get_state_list,request.POST,request.FILES)
        # form=AddStudentForm(request.POST,request.FILES)

        
        if form.is_valid():
            email_exists=True if (CustomUser.objects.filter(email=form.cleaned_data["email"]).exists()) else False
            # username_exists=True if (CustomUser.objects.filter(username=form.cleaned_data["username"]).exists()) else False
            if not email_exists:                            
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
                return HttpResponseRedirect(reverse("add_student"))

            else:
                messages.error(request,"Username or Email already exists")
                return HttpResponseRedirect(reverse("add_student"))
            # except:
            #     messages.error(request,"Failed to Add Student")
            #     return HttpResponseRedirect(reverse("add_student"))
        else:
            # form=AddStudentForm(request=request)
            # form=AddStudentForm(request.POST)
            form=AddStudentForm(get_course_list,get_session_list,get_country_list,get_state_list,request.POST)
            return render(request,"hod_template/add_student_template.html",{"form":form})


def delete_student(request,student_id):
    student = Students.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')

def add_subject(request):
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject_template.html",{"staffs":staffs,"courses":courses})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        if request.POST.get('subject_name')=="":
            messages.error(request, "Failed to Add Subject!")
            return HttpResponseRedirect("add_subject")
        else:
            subject_name=request.POST.get("subject_name")
            course=request.POST.get("course")
            course=Courses.objects.get(id=course)
            staff=request.POST.get("staff")
            staff=CustomUser.objects.get(id=staff)

        try:
            subject=Subjects(subject_name=subject_name,course=course,staff=staff)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))

def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_template/manage_staff_template.html",{"staffs":staffs})

def manage_student(request):
    students=Students.objects.all()
    return render(request,"hod_template/manage_student_template.html",{"students":students})

def college_student(request):
    students=Students.objects.all()
    return render(request,"hod_template/college_student_template.html",{"students":students})


def manage_course(request):
    courses=Courses.objects.all()
    return render(request,"hod_template/manage_course_template.html",{"courses":courses})

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,"hod_template/manage_subject_template.html",{"subjects":subjects})




def admin_notice(request):    
    if request.user.is_authenticated:
        notice = Notice.objects.all()
        form=addNoticeform()
        if(request.method=='POST'):
            form=addNoticeform(request.POST)
            if(form.is_valid()):
                form.save()
                return HttpResponseRedirect(reverse("admin_notice"))
        context={'form':form,'notice':notice,}
        return render(request,'hod_template/admin_notice.html',context)
    else: 
        return HttpResponseRedirect(reverse("admin_notice"))     



def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"hod_template/edit_staff_template.html",{"staff":staff,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def edit_student(request,student_id):
    states=[]
    request.session['student_id']=student_id
    student=Students.objects.get(admin=student_id)
    form=EditStudentForm(get_course_list,get_session_list,get_country_list,get_state_list)
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['profile_pic'].initial=student.profile_pic
    form.fields['course'].initial=student.course.id
    form.fields['gender'].initial=student.gender
    form.fields['prn_number'].initial=student.prn_number
    form.fields['currency_type'].initial=student.currency_type
    form.fields['father_name'].initial=student.father_name
    form.fields['mother_name'].initial=student.mother_name
    form.fields['alternate_mobile'].initial=student.alternate_mobile
    form.fields['date_of_birth'].initial=student.date_of_birth
    form.fields['admission_type'].initial=student.admission_type
    form.fields['admission_status'].initial=student.admission_type
    form.fields['permanent_address'].initial=student.permanent_address
    form.fields['communication_address'].initial=student.communication_address

    form.fields['country'].initial=student.country.id
    form.fields['state'].initial=student.state.id
    form.fields['mobile'].initial=student.mobile
    form.fields['session_year'].initial=student.session_year.id
    form.fields['session_joining_month'].initial=student.session_joining_month
    form.fields['final_fees'].initial=student.final_fees
    form.fields['other_information'].initial=student.other_information
    form.fields['highest_qualification'].initial=student.highest_qualification
    return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_student_save(request):
    # breakpoint()
    if request.method !="POST":
        return HttpResponse("<h2>Method Not allowed</h2>")
    else:
        student_id=request.session.get("student_id")
        if student_id==None:
            return HttpResponseRedirect("manage_student")

        # breakpoint()
        form=EditStudentForm(get_course_list,get_session_list,get_country_list,get_state_list,request.POST,request.FILES)
        
        
        
        if form.is_valid():
            # breakpoint()

            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            prn_number = form.cleaned_data["prn_number"]
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

            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None

            try:
                # breakpoint()
                user=CustomUser.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                student=Students.objects.get(admin=student_id)
                student.father_name=father_name
                student.mother_name=mother_name
                student.alternate_mobile=alternate_mobile
                student.prn_number=prn_number
                student.date_of_birth=date_of_birth
                student.admission_type=admission_type
                student.admission_status=admission_status
                student.permanent_address=permanent_address
                student.communication_address=communication_address

                country = Country.objects.get(id=country)
                student.country=country
                state = State.objects.get(id=state)
                student.state=state
                session_year = SessionYearModel.object.get(id=session_year)
                student.session_year = session_year
                student.mobile=mobile
                student.highest_qualification=highest_qualification
                student.session_joining_month=session_joining_month
                student.final_fees=final_fees
                student.other_information=other_information
                course=Courses.objects.get(id=course)
                student.course=course
                student.gender=gender
                student.currency_type=currency_type
                if profile_pic_url!=None:
                    student.profile_pic=profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request,"Successfully Edited Student Record")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed to Edit Student Record")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(get_course_list,get_session_list,get_country_list,get_state_list,request.POST,request.FILES)
            student=Students.objects.get(admin=student_id)
            return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})



def college_document(request,student_id):
    # breakpoint()
    request.session['student_id']=student_id
    student=Students.objects.get(admin=student_id)
    clg_documents_exists=CollegeDocument.objects.filter(student_id=student).exists()
    if clg_documents_exists == False:
            clg_documents=CollegeDocument.objects.create(student_id=student)
    else:
        clg_documents=CollegeDocument.objects.get(student_id=student)
    
    
    return render(request,"hod_template/college_document.html",{"clg_documents":clg_documents,"student":student})

def college_document_save(request):
    student_id=request.session.get("student_id")
    if student_id==None:
        return HttpResponseRedirect("college_student")
    
    admission_letter_url= None
    first_installment_url= None
    second_installment_url= None
    third_installment_url= None
    fourth_installment_url= None
    fifth_installment_url= None
    sixth_installment_url= None
    seventh_installment_url= None
    eighth_installment_url= None
    first_semester_url= None
    second_semester_url= None
    third_semester_url= None
    fourth_semester_url= None
    fifth_semester_url= None
    sixth_semester_url= None
    seventh_semester_url= None
    eighth_semester_url= None
    other_documents_url= None
    other_documents_one_url= None
    other_documents_two_url= None
    

    if request.method!="POST":
        return HttpResponseRedirect(reverse("college_document"))
    else:
        admission_letter=request.POST.get("admission_letter")
        admission_comment=request.POST.get("admission_comment")
        first_installment=request.POST.get("first_installment")
        one_comment=request.POST.get("one_comment")
        second_installment=request.POST.get("second_installment")
        two_comment=request.POST.get("two_comment")
        third_installment=request.POST.get("third_installment")
        three_comment=request.POST.get("three_comment")
        fourth_installment=request.POST.get("fourth_installment")
        four_comment=request.POST.get("four_comment")
        fifth_installment=request.POST.get("fifth_installment")
        five_comment=request.POST.get("five_comment")
        sixth_installment=request.POST.get("sixth_installment")
        six_comment=request.POST.get("six_comment")
        seventh_installment=request.POST.get("seventh_installment")
        seven_comment=request.POST.get("seven_comment")
        eighth_installment=request.POST.get("eighth_installment")
        eight_comment=request.POST.get("eight_comment")

        first_semester=request.POST.get("first_semester")
        first_comment=request.POST.get("first_comment")

        second_semester=request.POST.get("second_semester")
        second_comment=request.POST.get("second_comment")

        third_semester=request.POST.get("third_semester")
        third_comment=request.POST.get("third_comment")

        fourth_semester=request.POST.get("fourth_semester")
        fourth_comment=request.POST.get("fourth_comment")

        fifth_semester=request.POST.get("fifth_semester")
        fifth_comment=request.POST.get("fifth_comment")

        sixth_semester=request.POST.get("sixth_semester")
        sixth_comment=request.POST.get("sixth_comment")

        seventh_semester=request.POST.get("seventh_semester")
        seventh_comment=request.POST.get("seventh_comment")

        eighth_semester=request.POST.get("eighth_semester")
        eighth_comment=request.POST.get("eighth_comment")

        other_documents=request.POST.get("other_documents")
        other_comment=request.POST.get("other_comment")

        other_documents_one=request.POST.get("other_documents_one")
        other_comment_one=request.POST.get("other_comment_one")

        other_documents_two=request.POST.get("other_documents_two")
        other_comment_two=request.POST.get("other_comment_two")
        # breakpoint()
        
        try:
            # breakpoint()
            if request.FILES.get('admission_letter',False):
                admission_letter=request.FILES['admission_letter']
                fs=FileSystemStorage()
                filename=fs.save(admission_letter.name,admission_letter)
                admission_letter_url=fs.url(filename)
            
            if request.FILES.get('first_installment',False):
                first_installment=request.FILES['first_installment']
                fs=FileSystemStorage()
                filename=fs.save(first_installment.name,first_installment)
                first_installment_url=fs.url(filename)

            if request.FILES.get('second_installment',False):
                second_installment=request.FILES['second_installment']
                fs=FileSystemStorage()
                filename=fs.save(second_installment.name,second_installment)
                second_installment_url=fs.url(filename)

            if request.FILES.get('third_installment',False):
                third_installment=request.FILES['third_installment']
                fs=FileSystemStorage()
                filename=fs.save(third_installment.name,third_installment)
                third_installment_url=fs.url(filename)

            if request.FILES.get('fourth_installment',False):
                fourth_installment=request.FILES['fourth_installment']
                fs=FileSystemStorage()
                filename=fs.save(fourth_installment.name,fourth_installment)
                fourth_installment_url=fs.url(filename)

            if request.FILES.get('fifth_installment',False):
                fifth_installment=request.FILES['fifth_installment']
                fs=FileSystemStorage()
                filename=fs.save(fifth_installment.name,fifth_installment)
                fifth_installment_url=fs.url(filename)

            if request.FILES.get('sixth_installment',False):
                sixth_installment=request.FILES['sixth_installment']
                fs=FileSystemStorage()
                filename=fs.save(sixth_installment.name,sixth_installment)
                sixth_installment_url=fs.url(filename)

            if request.FILES.get('seventh_installment',False):
                seventh_installment=request.FILES['seventh_installment']
                fs=FileSystemStorage()
                filename=fs.save(seventh_installment.name,seventh_installment)
                seventh_installment_url=fs.url(filename)

            if request.FILES.get('eighth_installment',False):
                eighth_installment=request.FILES['eighth_installment']
                fs=FileSystemStorage()
                filename=fs.save(eighth_installment.name,eighth_installment)
                eighth_installment_url=fs.url(filename)

            if request.FILES.get('first_semester',False):
                first_semester=request.FILES['first_semester']
                fs=FileSystemStorage()
                filename=fs.save(first_semester.name,first_semester)
                first_semester_url=fs.url(filename)

            if request.FILES.get('second_semester',False):
                second_semester=request.FILES['second_semester']
                fs=FileSystemStorage()
                filename=fs.save(second_semester.name,second_semester)
                second_semester_url=fs.url(filename)

            if request.FILES.get('third_semester',False):
                third_semester=request.FILES['third_semester']
                fs=FileSystemStorage()
                filename=fs.save(third_semester.name,third_semester)
                third_semester_url=fs.url(filename)

            if request.FILES.get('fourth_semester',False):
                fourth_semester=request.FILES['fourth_semester']
                fs=FileSystemStorage()
                filename=fs.save(fourth_semester.name,fourth_semester)
                fourth_semester_url=fs.url(filename)

            if request.FILES.get('fifth_semester',False):
                fifth_semester=request.FILES['fifth_semester']
                fs=FileSystemStorage()
                filename=fs.save(fifth_semester.name,fifth_semester)
                fifth_semester_url=fs.url(filename)

            if request.FILES.get('sixth_semester',False):
                sixth_semester=request.FILES['sixth_semester']
                fs=FileSystemStorage()
                filename=fs.save(sixth_semester.name,sixth_semester)
                sixth_semester_url=fs.url(filename)

            if request.FILES.get('seventh_semester',False):
                seventh_semester=request.FILES['seventh_semester']
                fs=FileSystemStorage()
                filename=fs.save(seventh_semester.name,seventh_semester)
                seventh_semester_url=fs.url(filename)

            if request.FILES.get('eighth_semester',False):
                eighth_semester=request.FILES['eighth_semester']
                fs=FileSystemStorage()
                filename=fs.save(eighth_semester.name,eighth_semester)
                eighth_semester_url=fs.url(filename)

            if request.FILES.get('other_documents',False):
                other_documents=request.FILES['other_documents']
                fs=FileSystemStorage()
                filename=fs.save(other_documents.name,other_documents)
                other_documents_url=fs.url(filename)

            if request.FILES.get('other_documents_one',False):
                other_documents_one=request.FILES['other_documents_one']
                fs=FileSystemStorage()
                filename=fs.save(other_documents_one.name,other_documents_one)
                other_documents_one_url=fs.url(filename)

            if request.FILES.get('other_documents_two',False):
                other_documents_two=request.FILES['other_documents_two']
                fs=FileSystemStorage()
                filename=fs.save(other_documents_two.name,other_documents_two)
                other_documents_two_url=fs.url(filename)
            

            # breakpoint()
            # customuser=CustomUser.objects.get(id=request.user.id)
            student=Students.objects.get(admin=student_id)
            # stud_document=StudentDocument.objects.filter(student_id=student)
            # StudentDocument.objects.create(student_id=student,hsc_marksheet=hsc_marksheet_url)
            if CollegeDocument.objects.filter(student_id=student).exists(): 
                clg_document=CollegeDocument.objects.get(student_id=student)

                
                if admission_letter_url!=None:
                    clg_document.admission_letter=admission_letter_url
                    clg_document.admission_comment=admission_comment
                    clg_document.save()


                if first_installment!=None:
                    clg_document.first_installment=first_installment_url
                    clg_document.one_comment=one_comment
                    clg_document.save()

                if second_installment!=None:
                    clg_document.second_installment=second_installment_url
                    clg_document.two_comment=two_comment
                    clg_document.save()

                if third_installment!=None:
                    clg_document.third_installment=third_installment_url
                    clg_document.three_comment=three_comment
                    clg_document.save()

                if fourth_installment!=None:
                    clg_document.fourth_installment=fourth_installment_url
                    clg_document.four_comment=four_comment
                    clg_document.save()

                if fifth_installment!=None:
                    clg_document.fifth_installment=fifth_installment_url
                    clg_document.five_comment=five_comment
                    clg_document.save()

                if sixth_installment!=None:
                    clg_document.sixth_installment=sixth_installment_url
                    clg_document.six_comment=six_comment
                    clg_document.save()

                if seventh_installment!=None:
                    clg_document.seventh_installment=seventh_installment_url
                    clg_document.seven_comment=seven_comment
                    clg_document.save()

                if eighth_installment!=None:
                    clg_document.eighth_installment=eighth_installment_url
                    clg_document.eight_comment=eight_comment
                    clg_document.save()

                if first_semester_url!=None:
                    clg_document.first_semester=first_semester_url
                    clg_document.first_comment=first_comment
                    clg_document.save()

                if second_semester_url!=None:
                    clg_document.second_semester=second_semester_url
                    clg_document.second_comment=second_comment
                    clg_document.save()

                if third_semester_url!=None:
                    clg_document.third_semester=third_semester_url
                    clg_document.third_comment=third_comment
                    clg_document.save()

                if fourth_semester_url!=None:
                    clg_document.fourth_semester=fourth_semester_url
                    clg_document.fourth_comment=fourth_comment
                    clg_document.save()

                if fifth_semester_url!=None:
                    clg_document.fifth_semester=fifth_semester_url
                    clg_document.fifth_comment=fifth_comment
                    clg_document.save()

                if sixth_semester_url!=None:
                    clg_document.exam_results=first_semester_url
                    clg_document.sixth_comment=sixth_comment
                    clg_document.save()

                if seventh_semester_url!=None:
                    clg_document.seventh_semester=seventh_semester_url
                    clg_document.seventh_comment=seventh_comment
                    clg_document.save()

                if eighth_semester_url!=None:
                    clg_document.eighth_semester=eighth_semester_url
                    clg_document.eighth_comment=eighth_comment
                    clg_document.save()

                if other_documents_url!=None:
                    clg_document.other_documents=other_documents_url
                    clg_document.other_comment=other_comment
                    clg_document.save()

                if other_documents_one_url!=None:
                    clg_document.other_documents_one=other_documents_one_url
                    clg_document.other_comment_one=other_comment_one
                    clg_document.save()

                if other_documents_two_url!=None:
                    clg_document.other_documents_two=other_documents_two_url
                    clg_document.other_comment_two=other_comment_two
                    clg_document.save()

            else:
                # breakpoint()
                CollegeDocument.objects.create(student_id=student,admission_letter=admission_letter_url,admission_comment=admission_comment,first_installment=first_installment_url,one_comment=one_comment,second_installment=second_installment_url,two_comment=two_comment,third_installment=third_installment_url,three_comment=three_comment,fourth_installment=fourth_installment_url,four_comment=four_comment,fifth_installment=fifth_installment_url,five_comment=five_comment,sixth_installment=sixth_installment_url,six_comment=six_comment,seventh_installment=seventh_installment_url,seven_comment=seven_comment,eighth_installment=eighth_installment_url,eight_comment=eight_comment,first_semester=first_semester_url,first_comment=first_comment,second_semester=second_semester_url,second_comment=second_comment,third_semester=third_semester_url,third_comment=third_comment,fourth_semester=fourth_semester_url,fourth_comment=fourth_comment,fifth_semester=fifth_semester_url,fifth_comment=fifth_comment,sixth_semester=sixth_semester_url,sixth_comment=sixth_comment,seventh_semester=seventh_semester_url,seventh_comment=seventh_comment,eighth_semester=eighth_semester_url,eighth_comment=eighth_comment,other_documents=other_documents_url,other_comment=other_comment,other_documents_one=other_documents_one_url,other_comment_one=other_comment_one,other_documents_two=other_documents_two_url,other_comment_two=other_comment_two)

            # breakpoint()
            messages.success(request, "Successfully Uploaded document")
            return HttpResponseRedirect(reverse("college_document",kwargs={"student_id":student_id}))            
        except:
            
            messages.error(request, "Failed to Uploaded document")
            return HttpResponseRedirect(reverse("college_document",kwargs={"student_id":student_id}))


def hod_document(request,student_id):
    # breakpoint()
    request.session['student_id']=student_id
    student=Students.objects.get(admin=student_id)
    std_documents_exists=StudentDocument.objects.filter(student_id=student).exists()
    if std_documents_exists == False:
            std_documents=StudentDocument.objects.create(student_id=student)
    else:
        std_documents=StudentDocument.objects.get(student_id=student)
    
    
    return render(request,"hod_template/hod_document.html",{"std_documents":std_documents,"student":student})


def hod_document_save(request):
    # breakpoint()
    # request.session['student_id']=student_id
    student_id=request.session.get("student_id")
    if student_id==None:
        return HttpResponseRedirect("manage_student")
    
    hsc_marksheet_url= None
    hsc_certificate_url= None
    ssc_marksheet_url= None
    ssc_certificate_url= None
    ug_marksheet_url= None
    ug_certificate_url= None
    pg_marksheet_url= None
    pg_certificate_url= None
    diploma_marksheet_url= None
    diploma_certificate_url= None
    
    migration_url = None
    gap_url = None
    
    residence_url = None
    pan_card_url = None
    aadhar_card_url = None
    affidavit_url = None
    
    
    other_doc_one_url = None
    other_doc_two_url = None
    other_doc_three_url = None
    photo_url = None
    signature_url = None

    if request.method!="POST":
        return HttpResponseRedirect(reverse("hod_document"))
    else:
        hsc_marksheet=request.POST.get("hsc_marksheet")
        hsc_certificate=request.POST.get("hsc_certificate")
        ssc_marksheet=request.POST.get("ssc_marksheet")
        ssc_certificate=request.POST.get("ssc_certificate")
        ug_marksheet=request.POST.get("ug_marksheet")
        ug_certificate=request.POST.get("ug_certificate")
        pg_marksheet=request.POST.get("pg_marksheet")
        pg_certificate=request.POST.get("pg_certificate")
        diploma_marksheet=request.POST.get("diploma_marksheet")
        diploma_certificate=request.POST.get("diploma_certificate")
        
        migration=request.POST.get("migration")
        gap=request.POST.get("gap")
       
        residence=request.POST.get("residence")
        pan_card=request.POST.get("pan_card")
        aadhar_card=request.POST.get("aadhar_card")
        affidavit=request.POST.get("affidavit")
        
        other_doc_one=request.POST.get("other_doc_one")
        other_one_comment=request.POST.get("other_one_comment")
        other_doc_two=request.POST.get("other_doc_two")
        other_two_comment=request.POST.get("other_two_comment")
        other_doc_three=request.POST.get("other_doc_three")
        other_three_comment=request.POST.get("other_three_comment")
        photo=request.POST.get("photo")
        signature=request.POST.get("signature")
        # breakpoint()
        
        try:
            if request.FILES.get('hsc_marksheet',False):
                hsc_marksheet=request.FILES['hsc_marksheet']
                fs=FileSystemStorage()
                filename=fs.save(hsc_marksheet.name,hsc_marksheet)
                hsc_marksheet_url=fs.url(filename)
            
            if request.FILES.get('hsc_certificate',False):
                hsc_certificate=request.FILES['hsc_certificate']
                fs=FileSystemStorage()
                filename=fs.save(hsc_certificate.name,hsc_certificate)
                hsc_certificate_url=fs.url(filename)

            if request.FILES.get('ssc_marksheet',False):
                ssc_marksheet=request.FILES['ssc_marksheet']
                fs=FileSystemStorage()
                filename=fs.save(ssc_marksheet.name,ssc_marksheet)
                ssc_marksheet_url=fs.url(filename)

            if request.FILES.get('ssc_certificate',False):
                ssc_certificate=request.FILES['ssc_certificate']
                fs=FileSystemStorage()
                filename=fs.save(ssc_certificate.name,ssc_certificate)
                ssc_certificate_url=fs.url(filename)
            
            if request.FILES.get('ug_marksheet',False):
                ug_marksheet=request.FILES['ug_marksheet']
                fs=FileSystemStorage()
                filename=fs.save(ug_marksheet.name,ug_marksheet)
                ug_marksheet_url=fs.url(filename)

            if request.FILES.get('ug_certificate',False):
                ug_certificate=request.FILES['ug_certificate']
                fs=FileSystemStorage()
                filename=fs.save(ug_certificate.name,ug_certificate)
                ug_certificate_url=fs.url(filename)

            if request.FILES.get('pg_marksheet',False):
                pg_marksheet=request.FILES['pg_marksheet']
                fs=FileSystemStorage()
                filename=fs.save(pg_marksheet.name,pg_marksheet)
                pg_marksheet_url=fs.url(filename)

            if request.FILES.get('pg_certificate',False):
                pg_certificate=request.FILES['pg_certificate']
                fs=FileSystemStorage()
                filename=fs.save(pg_certificate.name,pg_certificate)
                pg_certificate_url=fs.url(filename)

            if request.FILES.get('diploma_marksheet',False):
                diploma_marksheet=request.FILES['diploma_marksheet']
                fs=FileSystemStorage()
                filename=fs.save(diploma_marksheet.name,diploma_marksheet)
                diploma_marksheet_url=fs.url(filename)

            if request.FILES.get('diploma_certificate',False):
                diploma_certificate=request.FILES['diploma_certificate']
                fs=FileSystemStorage()
                filename=fs.save(diploma_certificate.name,diploma_certificate)
                diploma_certificate_url=fs.url(filename)

            # if request.FILES.get('cc',False):
            #     cc=request.FILES['cc']
            #     fs=FileSystemStorage()
            #     filename=fs.save(cc.name,cc)
            #     cc_url=fs.url(filename)

            # if request.FILES.get('tc',False):
            #     tc=request.FILES['tc']
            #     fs=FileSystemStorage()
            #     filename=fs.save(tc.name,tc)
            #     tc_url=fs.url(filename)

            if request.FILES.get('migration',False):
                migration=request.FILES['migration']
                fs=FileSystemStorage()
                filename=fs.save(migration.name,migration)
                migration_url=fs.url(filename)

            if request.FILES.get('gap',False):
                gap=request.FILES['gap']
                fs=FileSystemStorage()
                filename=fs.save(gap.name,gap)
                gap_url=fs.url(filename)

            # if request.FILES.get('medical',False):
            #     medical=request.FILES['medical']
            #     fs=FileSystemStorage()
            #     filename=fs.save(medical.name,medical)
            #     medical_url=fs.url(filename)

            

            if request.FILES.get('residence',False):
                residence=request.FILES['residence']
                fs=FileSystemStorage()
                filename=fs.save(residence.name,residence)
                residence_url=fs.url(filename)

            if request.FILES.get('pan_card',False):
                pan_card=request.FILES['pan_card']
                fs=FileSystemStorage()
                filename=fs.save(pan_card.name,pan_card)
                pan_card_url=fs.url(filename)

            if request.FILES.get('aadhar_card',False):
                aadhar_card=request.FILES['aadhar_card']
                fs=FileSystemStorage()
                filename=fs.save(aadhar_card.name,aadhar_card)
                aadhar_card_url=fs.url(filename)



            if request.FILES.get('affidavit',False):
                affidavit=request.FILES['affidavit']
                fs=FileSystemStorage()
                filename=fs.save(affidavit.name,affidavit)
                affidavit_url=fs.url(filename)

            # if request.FILES.get('fee_commitment',False):
            #     fee_commitment=request.FILES['fee_commitment']
            #     fs=FileSystemStorage()
            #     filename=fs.save(fee_commitment.name,fee_commitment)
            #     fee_commitment_url=fs.url(filename)

            # if request.FILES.get('checklist',False):
            #     checklist=request.FILES['checklist']
            #     fs=FileSystemStorage()
            #     filename=fs.save(checklist.name,checklist)
            #     checklist_url=fs.url(filename)

            # if request.FILES.get('anti_ragging',False):
            #     anti_ragging=request.FILES['anti_ragging']
            #     fs=FileSystemStorage()
            #     filename=fs.save(anti_ragging.name,anti_ragging)
            #     anti_ragging_url=fs.url(filename)

            if request.FILES.get('other_doc_one',False):
                other_doc_one=request.FILES['other_doc_one']
                fs=FileSystemStorage()
                filename=fs.save(other_doc_one.name,other_doc_one)
                other_doc_one_url=fs.url(filename)

            if request.FILES.get('other_doc_two',False):
                other_doc_two=request.FILES['other_doc_two']
                fs=FileSystemStorage()
                filename=fs.save(other_doc_two.name,other_doc_two)
                other_doc_two_url=fs.url(filename)

            if request.FILES.get('other_doc_three',False):
                other_doc_three=request.FILES['other_doc_three']
                fs=FileSystemStorage()
                filename=fs.save(other_doc_three.name,other_doc_three)
                other_doc_three_url=fs.url(filename)

            if request.FILES.get('photo',False):
                photo=request.FILES['photo']
                fs=FileSystemStorage()
                filename=fs.save(photo.name,photo)
                photo_url=fs.url(filename)

            if request.FILES.get('signature',False):
                signature=request.FILES['signature']
                fs=FileSystemStorage()
                filename=fs.save(signature.name,signature)
                signature_url=fs.url(filename)

            # breakpoint()
            # customuser=CustomUser.objects.get(id=request.user.id)
            student=Students.objects.get(admin=student_id)
            # stud_document=StudentDocument.objects.filter(student_id=student)
            # StudentDocument.objects.create(student_id=student,hsc_marksheet=hsc_marksheet_url)
            if StudentDocument.objects.filter(student_id=student).exists(): 
                stud_document=StudentDocument.objects.get(student_id=student)
                
                if hsc_marksheet_url!=None:
                    stud_document.hsc_marksheet=hsc_marksheet_url
                    stud_document.save()

                if hsc_certificate_url!=None:
                    stud_document.hsc_certificate=hsc_certificate_url
                    stud_document.save()

                if ssc_marksheet_url!=None:
                    stud_document.ssc_marksheet=ssc_marksheet_url
                    stud_document.save()

                if ssc_certificate_url!=None:
                    stud_document.ssc_certificate=ssc_certificate_url
                    stud_document.save()

                if ug_marksheet_url!=None:
                    stud_document.ug_marksheet=ug_marksheet_url
                    stud_document.save()

                if ug_certificate_url!=None:
                    stud_document.ug_certificate=ug_certificate_url
                    stud_document.save()

                if pg_marksheet_url!=None:
                    stud_document.pg_marksheet=pg_marksheet_url
                    stud_document.save()

                if pg_certificate_url!=None:
                    stud_document.pg_certificate=pg_certificate_url
                    stud_document.save()

                if diploma_marksheet_url!=None:
                    stud_document.diploma_marksheet=diploma_marksheet_url
                    stud_document.save()

                if diploma_certificate_url!=None:
                    stud_document.diploma_certificate=diploma_certificate_url
                    stud_document.save()

                # if cc_url!=None:
                #     stud_document.cc=cc_url
                #     stud_document.save()

                
                # if tc_url!=None:
                #     stud_document.tc=tc_url
                #     stud_document.save()

                if migration_url!=None:
                    stud_document.migration=migration_url
                    stud_document.save()

                if gap_url!=None:
                    stud_document.gap=gap_url
                    stud_document.save()

                # if medical_url!=None:
                #     stud_document.medical=medical_url
                #     stud_document.save()


                if residence_url!=None:
                    stud_document.residence=residence_url
                    stud_document.save()

                if pan_card!=None:
                    stud_document.pan_card=pan_card_url
                    stud_document.save()

                if aadhar_card_url!=None:
                    stud_document.aadhar_card=aadhar_card_url
                    stud_document.save()

                if affidavit!=None:
                    stud_document.affidavit=affidavit_url
                    stud_document.save()

                # if fee_commitment!=None:
                #     stud_document.fee_commitment=fee_commitment_url
                #     stud_document.save()

                # if checklist!=None:
                #     stud_document.checklist=checklist_url
                #     stud_document.save()

                # if anti_ragging!=None:
                #     stud_document.anti_ragging=anti_ragging_url
                #     stud_document.save()

                if other_doc_one_url!=None:
                    stud_document.other_doc_one=other_doc_one_url
                    stud_document.other_one_comment=other_one_comment
                    stud_document.save()

                if other_doc_two_url!=None:
                    stud_document.other_doc_two=other_doc_two_url
                    stud_document.other_two_comment=other_two_comment
                    stud_document.save()

                if other_doc_three_url!=None:
                    stud_document.other_doc_three=other_doc_three_url
                    stud_document.other_three_comment=other_three_comment
                    stud_document.save()

                if photo!=None:
                    stud_document.photo=photo_url
                    stud_document.save()

                if signature!=None:
                    stud_document.signature=signature_url
                    stud_document.save()

            else:
                StudentDocument.objects.create(student_id=student,hsc_marksheet=hsc_marksheet_url,hsc_certificate=hsc_certificate_url,ssc_marksheet=ssc_marksheet_url,ssc_certificate=ssc_certificate_url,ug_marksheet=ug_marksheet_url,ug_certificate=ug_certificate_url,pg_marksheet=pg_marksheet_url,pg_certificate=pg_certificate_url,diploma_marksheet=diploma_marksheet_url,diploma_certificate=diploma_certificate_url,migration=migration_url,gap=gap_url,residence=residence_url,pan_card=pan_card_url,aadhar_card=aadhar_card_url,affidavit=affidavit_url,other_doc_one=other_doc_one_url,other_one_comment=other_one_comment,other_doc_two=other_doc_two_url,other_two_comment=other_two_comment,other_doc_three=other_doc_three_url,other_three_comment=other_three_comment,photo=photo_url,signature=signature_url)

            messages.success(request, "Successfully Uploaded document")
            return HttpResponseRedirect(reverse("hod_document",kwargs={"student_id":student_id}))            
        except:
            messages.error(request, "Failed to Uploaded document")
            return HttpResponseRedirect(reverse("hod_document",kwargs={"student_id":student_id}))


def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/edit_subject_template.html",{"subject":subject,"staffs":staffs,"courses":courses,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        staff_id=request.POST.get("staff")
        course_id=request.POST.get("course")

        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            staff=CustomUser.objects.get(id=staff_id)
            subject.staff_id=staff
            course=Courses.objects.get(id=course_id)
            subject.course_id=course
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course_template.html",{"course":course,"id":course_id})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course")
    try:
        course=Courses.objects.get(id=course_id)
        course.course_name=course_name
        course.save()
        messages.success(request,"Successfully Edited Course")
        return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
    except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))

def manage_session(request):
    return render(request,"hod_template/manage_session_template.html")

def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")

        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))


def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"hod_template/admin_profile.html",{"user":user})

def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            # if password!=None and password!="":
            #     customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_course_exist(request):
    course=request.POST.get("course")
    course_obj=Courses.objects.filter(course=course).exists()
    if course_obj:
        return HttpResponse("Course already exists!")
    else:
        return HttpResponse(False)

def get_course_list():
    courses = []
    try:
        list_courses = Courses.objects.all()
        for course in list_courses:
            small_course=(course.id,course.course_name)
            courses.append(small_course)

    except:
        courses = []

    return courses

def get_session_list():
    sessions = []
    try:
        session_list = SessionYearModel.object.all()

        for ses in session_list:
            small_ses = (ses.id, str(ses.session_start_year)+"   TO  "+str(ses.session_end_year))
            sessions.append(small_ses)
    except:
        sessions=[]

    return sessions

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
