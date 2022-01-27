import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls.base import reverse
import student_management_app
from student_management_app.forms import EditStudentForm, EditStudentProfile, addNoticeform

from student_management_app.models import Attendance, AttendanceReport, CollegeDocument, Country, Courses, CustomUser, FeedBackStudent, LeaveReportStudent, Links, Notice, SessionYearModel, State, StudentDocument, Students, Subjects


def student_home(request):
    user=CustomUser.objects.get(id=request.user.id)
    # student_objct=Students.objects.get(admin=user)
    students=Students.objects.filter(admin=user)
    notice = Notice.objects.all()
    student_obj=Students.objects.get(admin=request.user.id)
    attendance_total=AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present=AttendanceReport.objects.filter(student_id=student_obj,status=True).count()
    attendance_absent=AttendanceReport.objects.filter(student_id=student_obj,status=False).count()
    course=Courses.objects.get(id=student_obj.course.id)
    subjects=Subjects.objects.filter(course_id=course).count()
    subjects_data=Subjects.objects.filter(course_id=course)
    session_obj=SessionYearModel.object.get(id=student_obj.session_year.id)
    

    subject_name=[]
    data_present=[]
    data_absent=[]
    subject_data=Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance=Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=True,student_id=student_obj.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=False,student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    return render(request,"student_template/student_home_template.html",{"total_attendance":attendance_total,"attendance_absent":attendance_absent,"attendance_present":attendance_present,"subjects":subjects,"data_name":subject_name,"data1":data_present,"data2":data_absent,"user":user,"students":students,"notice":notice })

def student_view_attendance(request):
    student=Students.objects.get(admin=request.user.id)
    course=student.course_id
    subjects=Subjects.objects.filter(course_id=course)
    return render(request,"student_template/student_view_attendance.html",{"subjects":subjects})

def student_view_attendance_post(request):
    subject_id=request.POST.get("subject")
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")

    start_data_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_data_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    subject_obj=Subjects.objects.get(id=subject_id)
    user_object=CustomUser.objects.get(id=request.user.id)
    stud_obj=Students.objects.get(admin=user_object)

    attendance=Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse),subject_id=subject_obj)
    attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=stud_obj)
    return render(request,"student_template/student_attendance_data.html",{"attendance_reports":attendance_reports})


def student_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    student=Students.objects.get(admin=user)
    form=EditStudentProfile(get_course_list,get_session_list,get_country_list,get_state_list)
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    # form.fields['password'].initial=student.admin.password
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
    form.fields['work_experience'].initial=student.work_experience
    return render(request,"student_template/student_profile.html",{"user":user,"form":form,"student":student})

def states_change(request):
    # breakpoint()
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country=country_id)
    return render(request, 'edit_state_dropdown.html', {'states': states})

def student_profile_save(request):
    # breakpoint()
    if request.method !="POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        # student_id=request.session.get("student_id")
        # if student_id==None:
        #     return HttpResponseRedirect("manage_student")

        # breakpoint()
        form=EditStudentProfile(get_course_list,get_session_list,get_country_list,get_state_list,request.POST,request.FILES)
        
        
        
        if form.is_valid():
            # breakpoint()

            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            # email = form.cleaned_data["email"]
            # password = form.cleaned_data["password"]
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
            work_experience=form.cleaned_data["work_experience"]
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
                customuser=CustomUser.objects.get(id=request.user.id)
                customuser.first_name=first_name
                customuser.last_name=last_name
                customuser.username=username
                # customuser.email=email
                # customuser.password=password
                # if password!=None and password!="":
                #     customuser.set_password(password)
                customuser.save()

                student=Students.objects.get(admin=customuser)
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
                student.work_experience=work_experience
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
                
                messages.success(request,"Successfully Edited Student Record")
                return HttpResponseRedirect(reverse("student_profile"))
            except:
                messages.error(request,"Failed to Edit Student Record")
                return HttpResponseRedirect(reverse("student_profile"))
        # else:
        #     form=EditStudentProfile(get_course_list,get_session_list,get_country_list,get_state_list,request.POST,request.FILES)
        #     student=Students.objects.get(admin=user)
        #     return render(request,"hod_template/edit_student_template.html",{"form":form,"id":user,"username":student.admin.username})


def student_apply_leave(request):
    staff_obj = Students.objects.get(admin=request.user.id)
    leave_data=LeaveReportStudent.objects.filter(student_id=staff_obj)
    return render(request,"student_template/student_apply_leave.html",{"leave_data":leave_data})

def student_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        student_obj=Students.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportStudent(student_id=student_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))


def student_feedback(request):
    staff_id=Students.objects.get(admin=request.user.id)
    feedback_data=FeedBackStudent.objects.filter(student_id=staff_id)
    return render(request,"student_template/student_feedback.html",{"feedback_data":feedback_data})

def student_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        student_obj=Students.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackStudent(student_id=student_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))


def student_dashboard(request):
    user=CustomUser.objects.get(id=request.user.id)
    # student_objct=Students.objects.get(admin=user)
    students=Students.objects.filter(admin=user)
    # students=user.object.get(admin=Students)
    return render(request,"student_template/student_dashboard.html",{"user":user,"students":students})

def institute_document(request):
    clg_documents = None
    # request.session['student_id']=student_id
    user=CustomUser.objects.get(id=request.user.id)
    students=Students.objects.filter(admin=user).get()
    if students != None:
        clg_documents_exists= CollegeDocument.objects.filter(student_id=students).exists()
        if clg_documents_exists == False:
            clg_documents=CollegeDocument.objects.create(student_id=students)
        else:
            clg_documents=CollegeDocument.objects.get(student_id=students)

    return render(request,"student_template/institute_document.html",{"user":user,"students":students,"clg_documents":clg_documents})


def student_notice(request):    
    if request.user.is_authenticated:
        notice = Notice.objects.all()
        context={'notice':notice}
        return render(request,'student_template/student_notice.html',context)
    else: 
        return HttpResponseRedirect(reverse("student_notice")) 

def student_links(request):
    links=Links.objects.all()
    return render(request,"student_template/college_links.html",{"links":links})

def student_document(request):
    std_documents = None
    # request.session['student_id']=student_id
    user=CustomUser.objects.get(id=request.user.id)
    students=Students.objects.filter(admin=user).get()
    if students != None:
        std_documents_exists=StudentDocument.objects.filter(student_id=students).exists()
        if std_documents_exists == False:
            std_documents=StudentDocument.objects.create(student_id=students)
        else:
            std_documents=StudentDocument.objects.get(student_id=students)

    return render(request,"student_template/student_document.html",{"user":user,"students":students,"std_documents":std_documents})

def student_document_save(request):
    # student_id=request.session.get("student_id")
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
        return HttpResponseRedirect(reverse("student_document"))
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
        # other_one_comment=request.POST.get("other_one_comment")

        other_doc_two=request.POST.get("other_doc_two")
        # other_two_comment=request.POST.get("other_two_comment")

        other_doc_three=request.POST.get("other_doc_three")
        # other_three_comment=request.POST.get("other_three_comment")

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

            # if request.FILES.get('caste',False):
            #     caste=request.FILES['caste']
            #     fs=FileSystemStorage()
            #     filename=fs.save(caste.name,caste)
            #     caste_url=fs.url(filename)

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

            # if request.FILES.get('income',False):
            #     income=request.FILES['income']
            #     fs=FileSystemStorage()
            #     filename=fs.save(income.name,income)
            #     income_url=fs.url(filename)

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

            # if request.FILES.get('sk_form',False):
            #     sk_form=request.FILES['sk_form']
            #     fs=FileSystemStorage()
            #     filename=fs.save(sk_form.name,sk_form)
            #     sk_form_url=fs.url(filename)

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


            customuser=CustomUser.objects.get(id=request.user.id)
            student=Students.objects.get(admin=customuser)
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

                # if caste_url!=None:
                #     stud_document.caste=caste_url
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

                # if income_url!=None:
                #     stud_document.income=income_url
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

                # if sk_form!=None:
                #     stud_document.sk_form=sk_form_url
                #     stud_document.save()

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
                    # stud_document.other_one_comment=other_one_comment
                    stud_document.save()

                if other_doc_two_url!=None:
                    stud_document.other_doc_two=other_doc_two_url
                    # stud_document.other_two_comment=other_two_comment
                    stud_document.save()

                if other_doc_three_url!=None:
                    stud_document.other_doc_three=other_doc_three_url
                    # stud_document.other_three_comment=other_three_comment
                    stud_document.save()

                if photo!=None:
                    stud_document.photo=photo_url
                    stud_document.save()

                if signature!=None:
                    stud_document.signature=signature_url
                    stud_document.save()

            else:
                StudentDocument.objects.create(student_id_id=student,hsc_marksheet=hsc_marksheet_url,hsc_certificate=hsc_certificate_url,ssc_marksheet=ssc_marksheet_url,ssc_certificate=ssc_certificate_url,ug_marksheet=ug_marksheet_url,ug_certificate=ug_certificate_url,pg_marksheet=pg_marksheet_url,pg_certificate=pg_certificate_url,diploma_marksheet=diploma_marksheet_url,diploma_certificate=diploma_certificate_url,migration=migration_url,gap=gap_url,residence=residence_url,pan_card=pan_card_url,aadhar_card=aadhar_card_url,affidavit=affidavit_url,other_doc_one=other_doc_one_url,other_doc_two=other_doc_two_url,other_doc_three=other_doc_three_url,photo=photo_url,signature=signature_url)

            messages.success(request, "Successfully Uploaded document")
            return HttpResponseRedirect(reverse("student_document"))            
        except:
            messages.error(request, "Failed to Uploaded document")
            return HttpResponseRedirect(reverse("student_document"))


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
