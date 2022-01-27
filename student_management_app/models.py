from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import AutoField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.fields import IntegerField

# Create your models here.
class Comments(models.Model):
    id=models.AutoField(primary_key=True)
    created_at=models.DateTimeField(auto_now_add=True)
    message=models.CharField(max_length=255)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Country(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class State(models.Model):
    id=models.AutoField(primary_key=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SessionYearModel(models.Model):
    id=models.AutoField(primary_key=True)
    session_start_year=models.DateField()
    session_end_year=models.DateField()
    object=models.Manager()

class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"Staff"),(3,"Student"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Staffs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Subjects(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=255)
    course=models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
    staff=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Students(models.Model):
    class currencyType(models.TextChoices):
        DOLLAR ='USD'
        RUPEES ='INR'
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    prn_number=models.CharField(max_length=255)
    gender=models.CharField(max_length=255)
    father_name=models.CharField(max_length=255)
    mother_name=models.CharField(max_length=255)
    date_of_birth=models.DateField()
    admission_type=models.CharField(max_length=255)
    admission_status=models.CharField(max_length=255)
    session_year=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=255)
    alternate_mobile=models.CharField(max_length=255)
    permanent_address=models.TextField()
    communication_address=models.TextField()
    session_joining_month=models.CharField(max_length=255)
    highest_qualification=models.CharField(max_length=255)
    work_experience=models.CharField(max_length=255)
    currency_type=models.CharField(max_length=255)
    final_fees=models.CharField(max_length=255)
    other_information=models.CharField(max_length=255)
    profile_pic=models.FileField()
    course=models.ForeignKey(Courses,on_delete=models.DO_NOTHING)
    country=models.ForeignKey(Country,on_delete=models.DO_NOTHING,null=True)
    state=models.ForeignKey(State,on_delete=models.DO_NOTHING,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)    
    objects=models.Manager()

class StudentDocument(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    hsc_marksheet=models.FileField()
    check_hsc_marksheet=models.IntegerField(default=0)
    hsc_certificate=models.FileField()
    ssc_marksheet=models.FileField()
    ssc_certificate=models.FileField()
    ug_marksheet=models.FileField()
    ug_certificate=models.FileField()
    pg_marksheet=models.FileField()
    pg_certificate=models.FileField()
    diploma_marksheet=models.FileField()
    diploma_certificate=models.FileField()
    tc=models.FileField()
    migration=models.FileField()
    gap=models.FileField()
    medical=models.FileField()
    residence=models.FileField()
    pan_card=models.FileField()
    aadhar_card=models.FileField()

    
    affidavit=models.FileField()
    fee_commitment=models.FileField()
    checklist=models.FileField()
    anti_ragging=models.FileField()
    other_doc_one=models.FileField()
    other_one_comment=models.CharField(max_length=255)
    other_doc_two=models.FileField()
    other_two_comment=models.CharField(max_length=255)
    other_doc_three=models.FileField()
    other_three_comment=models.CharField(max_length=255)
    photo=models.FileField()
    signature=models.FileField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Subjects,on_delete=models.DO_NOTHING)
    attendance_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class LeaveReportStudent(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=255)
    leave_message=models.TextField()
    leave_status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Notice(models.Model):
    id = models.AutoField(primary_key=True)
    date=models.DateField(auto_now_add=True)
    by=models.CharField(max_length=50,null=True,default='IREF')
    message=models.CharField(max_length=500)

    def __str__(self):
        return self.message

class CollegeDocument(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    admission_letter=models.FileField()
    admission_comment=models.CharField(max_length=255)
    first_installment=models.FileField()
    one_comment=models.CharField(max_length=255)
    second_installment=models.FileField()
    two_comment=models.CharField(max_length=255)
    third_installment=models.FileField()
    three_comment=models.CharField(max_length=255)
    fourth_installment=models.FileField()
    four_comment=models.CharField(max_length=255)
    fifth_installment=models.FileField()
    five_comment=models.CharField(max_length=255)
    sixth_installment=models.FileField()
    six_comment=models.CharField(max_length=255)
    seventh_installment=models.FileField()
    seven_comment=models.CharField(max_length=255)
    eighth_installment=models.FileField()
    eight_comment=models.CharField(max_length=255)
    first_semester=models.FileField()
    first_comment=models.CharField(max_length=255)
    second_semester=models.FileField()
    second_comment=models.CharField(max_length=255)
    third_semester=models.FileField()
    third_comment=models.CharField(max_length=255)
    fourth_semester=models.FileField()
    fourth_comment=models.CharField(max_length=255)
    fifth_semester=models.FileField()
    fifth_comment=models.CharField(max_length=255)
    sixth_semester=models.FileField()
    sixth_comment=models.CharField(max_length=255)
    seventh_semester=models.FileField()
    seventh_comment=models.CharField(max_length=255)
    eighth_semester=models.FileField()
    eighth_comment=models.CharField(max_length=255)
    other_documents=models.FileField()
    other_comment=models.CharField(max_length=255)
    other_documents_one=models.FileField()
    other_comment_one=models.CharField(max_length=255)
    other_documents_two=models.FileField()
    other_comment_two=models.CharField(max_length=255)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Links(models.Model):
    class linkType(models.TextChoices):
        IMPORTANT_LINKS='IMPORTANT_LINKS'
        CLASS_LINKS='CLASS_LINKS'
    id=models.AutoField(primary_key=True)
    urls=models.URLField()
    name=models.CharField(max_length=255)
    comments=models.CharField(max_length=255)
    types=models.CharField(max_length=32,choices=linkType.choices)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)   
    objects=models.Manager()







@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Staffs.objects.create(admin=instance,address="")
        if instance.user_type==3:
            Students.objects.create(admin=instance,course=Courses.objects.get(id=1),session_year=SessionYearModel.object.get(id=1),country=Country.objects.get(id=1),state=State.objects.get(id=1),permanent_address="",communication_address="",mobile="",highest_qualification="",work_experience="",profile_pic="",gender="",father_name="",mother_name="",date_of_birth="2020-01-01",session_joining_month="",final_fees="",other_information="",admission_type="",admission_status="",currency_type="",prn_number="",alternate_mobile="")

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.staffs.save()
    if instance.user_type==3:
        instance.students.save()