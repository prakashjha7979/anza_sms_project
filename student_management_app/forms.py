from django import forms
from django.forms import ModelForm
from django.forms import ChoiceField
from student_management_app import models

from student_management_app.models import Country, Courses, SessionYearModel, State, Subjects, Students,Notice




class ChoiceNoValidation(ChoiceField):
    def validate(self, value):
        pass


class DateInput(forms.DateInput):
    input_type = "date"

class NumberInput(forms.NumberInput):
    input_type = "number"

class AddStudentForm(forms.Form): 
    def __init__(self,list_courses,session_list,country_list,State_list,*args,**kwargs):
        super(AddStudentForm,self).__init__(*args,**kwargs)
        self.fields['course'].choices = list_courses
        self.fields['session_year'].choices = session_list
        self.fields['country'].choices = country_list
        self.fields['state'].choices = State_list
        
        # breakpoint()
        # if 'country' in self.fields:
        #     try:
        #         country_id = int(self.fields.get('country'))
        #         self.fields['state'].queryset = State.objects.filter(country=country_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass  # invalid input from the client; ignore and fallback to empty City queryset
        # # elif self.instance.id:
        # #     self.fields['state'].queryset = self.instance.country.State_set.order_by('name')
        # else:
        #     self.fields['state'].queryset = State.objects.all().order_by('name')
       
    

        
        
    
    
    
    email=forms.EmailField(label="Email (*must required)",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    prn_number=forms.CharField(label="PRN(Permanent Registration Number)",max_length=20,widget=forms.NumberInput(attrs={"class":"form-control"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name(put the name as on  the previous marksheet)",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name(put the name as on  the previous marksheet)",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(required = False,label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))


    # country_detail=[] 
    # try:
    #     countries = Country.objects.all().order_by('-course_name')
    #     for country in countries:
    #         country_detail=(country.id,country.name)
    #         course_list.append(small_course)
    # except:
    #     course_list=[]
    



    
    gender_choice=(
        ("Male","Male"),
        ("Female","Female"),
        ("Other","Other")
    )

    currency_choice=(
        ("INR","INR"),
        ("USD","USD"),
       
    )

    admission_choice=(
        ("Full Time","Full Time"),
        ("Part Time","Part Time"),
        ("Distance","Distance"),
        ("Online","Online"),
        ("Diploma","Diploma"),
        ("Certification","Certification")
    )

    session_choice=(
        ("Jan","Jan"),
        ("Feb","Feb"),
        ("Mar","Mar"),
        ("Apr","Apr"),
        ("May","May"),
        ("Jun","Jun"),
        ("Jul","Jul"),
        ("Aug","Aug"),
        ("Sep","Sep"),
        ("Oct","Oct"),
        ("Nov","Nov"),
        ("Dec","Dec")
    )

    qualification_choice=(
        ("10","10"),
        ("10+2","10+2"),
        ("Diploma","Diploma"),
        ("Graduation","Graduation"),
        ("Post Graduation","Post Graduation"),
        ("Others","Others")
    )

    course=forms.ChoiceField(label="Course",widget=forms.Select(attrs={"class":"form-control"}))
    # course = forms.ChoiceField()
    gender=forms.ChoiceField(label="Gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    
    father_name=forms.CharField(label="Father name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    mother_name=forms.CharField(label="Mother name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    date_of_birth=forms.DateField(label="date_of_birth",widget=DateInput(attrs={"class":"form-control"}))
    admission_type=forms.ChoiceField(label="Admission type",choices=admission_choice,widget=forms.Select(attrs={"class":"form-control"}))
    admission_status=forms.CharField(label="admission status",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))

    country=forms.ChoiceField(label="Country",widget=forms.Select(attrs={"class":"form-control"}))
    state=forms.ChoiceField(label="State",widget=forms.Select(attrs={"class":"form-control"}))

    permanent_address=forms.CharField(label="permanent address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    communication_address=forms.CharField(label="communication address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    session_year=forms.ChoiceField(label="Session Year",widget=forms.Select(attrs={"class":"form-control"}))
    session_joining_month=forms.ChoiceField(label="Session Joining Month",choices=session_choice,widget=forms.Select(attrs={"class":"form-control"}))
    mobile=forms.CharField(label="mobile",max_length=20,widget=forms.NumberInput(attrs={"class":"form-control"}))
    alternate_mobile=forms.CharField(label="alternate mobile",max_length=20,widget=forms.NumberInput(attrs={"class":"form-control"}))
    highest_qualification=forms.ChoiceField(label="Highest qualification",choices=qualification_choice,widget=forms.Select(attrs={"class":"form-control"}))
    currency_type=forms.ChoiceField(label="Currency type",choices=currency_choice,widget=forms.Select(attrs={"class":"form-control"}))
    final_fees=forms.CharField(label="Final fees",max_length=50,widget=forms.NumberInput(attrs={"class":"form-control"}))
    other_information=forms.CharField(label="Other information",max_length=255,widget=forms.TextInput(attrs={"class":"form-control"}))
    

class EditStudentForm(forms.Form):
    # breakpoint()
    def __init__(self,list_courses,session_list,country_list,state_list,*args,**kwargs):
        super(EditStudentForm,self).__init__(*args,**kwargs)
        self.fields['course'].choices = list_courses
        self.fields['session_year'].choices = session_list
        self.fields['country'].choices = country_list
        self.fields['state'].choices = state_list
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    prn_number=forms.CharField(label="PRN(Permanent Registration Number)",max_length=20,widget=forms.NumberInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name(put the name as on  the previous marksheet)",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name(put the name as on  the previous marksheet)",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(required = False,label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False)


    # course_list=[]
    # try:
    #     courses = Courses.objects.all()
    #     for course in courses:
    #         small_course=(course.id,course.course_name)
    #         course_list.append(small_course)
    # except:
    #     course_list=[]

    # session_list = []
    # try:
    #     sessions = SessionYearModel.object.all()

    #     for ses in sessions:
    #         small_ses = (ses.id, str(ses.session_start_year)+"   TO  "+str(ses.session_end_year))
    #         session_list.append(small_ses)
    # except:
    #     session_list = []

    # countries=[]
    # try:
    #     country_list = Country.objects.all()

    #     for country in country_list:
    #         country_name=(country.id,country.name)
    #         countries.append(country_name)
            
    # except:
    #     countries=[]

    # state_list=[]
    # try:
    #     states = State.objects.all()
    #     for state in states:
    #         state_name=(state.id,state.name)
    #         state_list.append(state_name)
    # except:
    #     state_list=[]

    gender_choice=(
        ("Male","Male"),
        ("Female","Female"),
        ("Other","Other")
    )

    currency_choice=(
        ("INR","INR"),
        ("USD","USD"),
       
    )

    admission_choice=(
        ("Full Time","Part Time"),
        ("Part Time","Part Time"),
        ("Distance","Distance"),
        ("Online","Online"),
        ("Diploma","Diploma"),
        ("Certification","Certification")
    )

    session_choice=(
        ("Jan","Jan"),
        ("Feb","Feb"),
        ("Mar","Mar"),
        ("Apr","Apr"),
        ("May","May"),
        ("Jun","Jun"),
        ("Jul","Jul"),
        ("Aug","Aug"),
        ("Sep","Sep"),
        ("Oct","Oct"),
        ("Nov","Nov"),
        ("Dec","Dec")
    )

    qualification_choice=(
        ("10","10"),
        ("10+2","10+2"),
        ("Diploma","Diploma"),
        ("Graduation","Graduation"),
        ("Post Graduation","Post Graduation"),
        ("Others","Others")
    )

    course=forms.ChoiceField(label="Course",widget=forms.Select(attrs={"class":"form-control"}))
    gender=forms.ChoiceField(label="Gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    
    father_name=forms.CharField(label="Father name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    mother_name=forms.CharField(label="Mother name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    date_of_birth=forms.DateField(label="date_of_birth",widget=DateInput(attrs={"class":"form-control"}))
    admission_type=forms.ChoiceField(label="Admission type",choices=admission_choice,widget=forms.Select(attrs={"class":"form-control"}))
    admission_status=forms.CharField(label="admission status",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))

    country=forms.ChoiceField(label="Country",widget=forms.Select(attrs={"class":"form-control"}))
    state=forms.ChoiceField(label="State",widget=forms.Select(attrs={"class":"form-control"}))

    permanent_address=forms.CharField(label="permanent address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    communication_address=forms.CharField(label="communication address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    session_year=forms.ChoiceField(label="Session Year",widget=forms.Select(attrs={"class":"form-control"}))
    session_joining_month=forms.ChoiceField(label="Session Joining Month",choices=session_choice,widget=forms.Select(attrs={"class":"form-control"}))
    mobile=forms.CharField(label="mobile",max_length=50,widget=forms.NumberInput(attrs={"class":"form-control"}))
    alternate_mobile=forms.CharField(label="alternate mobile",max_length=20,widget=forms.NumberInput(attrs={"class":"form-control"}))
    highest_qualification=forms.ChoiceField(label="Highest qualification",choices=qualification_choice,widget=forms.Select(attrs={"class":"form-control"}))
    currency_type=forms.ChoiceField(label="Currency type",choices=currency_choice,widget=forms.Select(attrs={"class":"form-control"}))
    final_fees=forms.CharField(label="Final fees",max_length=50,widget=forms.NumberInput(attrs={"class":"form-control"}))
    other_information=forms.CharField(label="Other information",max_length=255,widget=forms.TextInput(attrs={"class":"form-control"}))

class AddCourseForm(forms.Form):
    course_name=forms.CharField(label="Course",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    
#for notice related form
class addNoticeform(ModelForm):
    class Meta:
        model=Notice
        fields="__all__"

# class NoticeForm(forms.Form):
#     message=forms.CharField(label="Message",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    # by=forms.CharField(label="By", max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
