from django.db import models
from multiselectfield import MultiSelectField
from django.utils.safestring import mark_safe
# Create your models here.

course_choices = (('Linux', 'Senior/Midium Level Linux',),
                  ('Python Fullstack', 'Senior Python Fullstack',),)

class_type_choice = (('fulltime', 'fulltime class',),
                     ('online', 'online class',),
                     ('weekend', 'weekend class',),)

source_type = (('qq', 'qq group',),
               ('referral', 'Intruduced by friend',),
               ('website', 'official website',),
               ('baidu_ads', 'baidu campaign',),
               ('office_direct', 'office enroll',),
               ('WoM', 'Koubei Software',),
               ('public_class', 'public class',),
               ('website_luffy', 'Luffy Website',),
               ('others', 'others',),)

enroll_status_choices = (('signed', 'Enrolled',),
                         ('unregistered', 'Unenrolled',),
                         ('studying', 'styding',),
                         ('paid_in_full', 'Paid Tuition',),)

seek_status_choice = (('A', 'No study plan recently',),
                      ('B', 'Enroll in 1 month',),
                      ('C', 'Enroll in 2 months',),
                      ('D', 'Enroll in 1 week',),
                      ('E', 'Paid deposit',),
                      ('F', 'Enrolled',),
                      ('G', 'Full Paid',),
                      ('H', 'Error',),)

pay_type_choices = (('deposit', 'Deposit',),
                    ('tuition', 'Tuition',),
                    ('transfer', 'Transfer Class Fee',),
                    ('dropout', 'Withdraw Class',),
                    ('refund', 'Refund',),)

attendance_choice = (('checked', 'In Class',),
                     ('vacate', 'Asked Leave',),
                     ('late', 'late',),
                     ('absence', 'Absence',),
                     ('leave_early', 'Leave Early',),)

score_choices = ((100, 'A+',),
                 (90, 'A',),
                 (85, 'B+',),
                 (80, 'B',),
                 (70, 'B-',),
                 (60, 'c+',),
                 (50, 'c',),
                 (40, 'c-',),
                 (0, 'D',),
                 (-1, 'N/A',),
                 (-100, 'Copy',),
                 (-1000, 'Fail',),)


class Department(models.Model):
    """
    Department Table
    """
    name = models.CharField(max_length=32, verbose_name="Department Name")
    count = models.IntegerField(verbose_name="Number of Staffs", default=0)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    username = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField('Name', max_length=32)
    department = models.ForeignKey('Department', default=None, blank=True, null=True)
    mobile = models.CharField('Mobile', max_length=32, default=None, blank=True, null=True)
    memo = models.TextField('Comment', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    qq = models.CharField('QQ', max_length=64, help_text='QQ Number must be unique')
    qq_name = models.CharField('QQ name', max_length=64, blank=True, null=True)
    name = models.CharField('Name', max_length=32, blank=True, null=True,
                            help_text="Student should use their real name after enrolled a course")
    sex_type = (('male', 'Male',), ('female', 'Female',),)
    sex = models.CharField('Gender', choices=sex_type, max_length=16, default='male', blank=True, null=True)
    birthday = models.DateField('D.O.B', default=None, help_text="Format yyyy-mm-dd", blank=True, null=True)
    phone = models.BigIntegerField('Phone Number', blank=True, null=True)
    source = models.CharField('Customer source statistic', max_length=64, choices=source_type, default='qq')
    introduce_from = models.ForeignKey('self', verbose_name='Introduced by other students', blank=True, null=True)
    course = MultiSelectField('Consulting Courses', choices=course_choices)
    class_type = models.CharField('Class Type', max_length=64, choices=class_type_choice, default='fulltime')
    customer_note = models.TextField('Customer Note', blank=True, null=True)
    status = models.CharField('Status', choices=enroll_status_choices, max_length=64, default='unregistered',
                              help_text='Current customer status')
    last_consult_date = models.DateField('The last contact date', auto_now_add=True)
    next_date = models.DateField('Expected next contact date', blank=True, null=True)
    consultant = models.ForeignKey('UserProfile', verbose_name='Sales', related_name='customers', blank=True, null=True)
    class_list = models.ManyToManyField('ClassList', verbose_name='Enrolled class',blank=True)

    def show_class(self):
        return "".join([str(i) for i in self.class_list.all()])

    def show_status(self):
        color_dic = {
            "signed":"green",
            "unregistered":"red",
            "studying":"blue",
            "paid_in_full":"gold"
        }

        return mark_safe(
            '<span style="color:white;background:{};padding:5px">{}</span>'.format(color_dic.get(self.status),self.get_status_display())
        )

    def __str__(self):
        return self.name

class Campus(models.Model):
    name = models.CharField(verbose_name='Campus', max_length=64)
    address = models.CharField(verbose_name='Address Details', max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name

class ClassList(models.Model):
    course = models.CharField('Course Name', max_length=64, choices=course_choices)
    semester = models.IntegerField('Semester')
    campuses = models.ForeignKey('Campus', verbose_name='Campus')
    price = models.IntegerField('Tuition', default=10000)
    memo = models.CharField('Introduction', blank=True, null=True, max_length=100)
    start_date = models.DateField('Commencement date')
    graduate_date = models.DateField('Graduate date', blank=True, null=True)
    teachers = models.ManyToManyField('UserProfile', verbose_name="Teacher")
    class_type = models.CharField(choices=class_type_choice, max_length=64, blank=True, null=True)

    def __str__(self):
        return "{}-{}".format(self.course,self.semester)

    class Meta:
        unique_together = ("course", "semester", "campuses")


class ConsultRecord(models.Model):
    customer = models.ForeignKey('Customer', verbose_name='Served Customer')
    note = models.TextField(verbose_name='Chatting history')
    status = models.CharField('Customer Status', max_length=8, choices=seek_status_choice,
                              help_text="Select the customer's status")
    consultant = models.ForeignKey('UserProfile', verbose_name='Consultant', related_name='records')
    date = models.DateTimeField('The last chat date', auto_now_add=True)
    delete_status = models.BooleanField(verbose_name='Delete Status', default=False)


class Enrollment(models.Model):
    why_us = models.TextField('Why chose us', max_length=1024, default=None, blank=True, null=True)
    your_expectation = models.TextField('Achievement expectation', max_length=1024, blank=True, null=True)
    contract_agree = models.BooleanField('I have read the contract and agreed its context', default=False)
    contract_approved = models.BooleanField('Audited',
                                            help_text="Check the selection after veryfied student's information")
    enrolled_date = models.DateTimeField(auto_now_add=True, verbose_name='Enrollment date')
    memo = models.TextField('Comment', blank=True, null=True)
    delete_status = models.BooleanField(verbose_name='Delete status', default=False)
    customer = models.ForeignKey('Customer', verbose_name='Customer name')
    school = models.ForeignKey('Campus')
    enrolment_class = models.ForeignKey('ClassList', verbose_name='Enrolled class')

    class Meta:
        unique_together = ('enrolment_class', 'customer')


class PaymentRecord(models.Model):
    pay_type = models.CharField("Payment Method", choices=pay_type_choices, max_length=64, default="deposit")
    paid_fee = models.IntegerField("Paid Amount", default=0)
    note = models.TextField("Note", blank=True, null=True)
    date = models.DateTimeField('Payment date', auto_now_add=True)
    course = models.CharField('Course Name', choices=course_choices, max_length=64, blank=True, null=True,
                              default='N/A')
    class_type = models.CharField('Class Type', choices=class_type_choice, max_length=64, blank=True, null=True,
                                  default="N/A")
    enrolment_class = models.ForeignKey('ClassList', verbose_name='Enrolled Class', blank=True, null=True)
    customer = models.ForeignKey('Customer', verbose_name='Customer')
    consultant = models.ForeignKey('UserProfile', verbose_name="Sales")
    delete_status = models.BooleanField(verbose_name='Delete Status', default=False)

    status_choices = (
        (1, 'unaudited'),
        (2, 'audited'),
    )
    status = models.IntegerField(verbose_name='Audit', default=1, choices=status_choices)
    confirm_date = models.DateTimeField(verbose_name="Confirm date", null=True, blank=True)
    confirm_user = models.ForeignKey(verbose_name="Confirmed by whom", to='UserProfile', related_name='confirms',
                                     null=True, blank=True)


class CourseRecord(models.Model):
    day_num = models.IntegerField('Class Order', help_text="Input a integer to show which class is it")
    date = models.DateTimeField(auto_now_add=True, verbose_name='Class date')
    course_title = models.CharField('Course Title', max_length=64, blank=True, null=True)
    course_memo = models.TextField('Course content', max_length=300, blank=True, null=True)
    has_homework = models.BooleanField(default=True, verbose_name='has homework')
    homework_title = models.CharField('Homework Title', max_length=64, blank=True, null=True)
    homework_memo = models.TextField('Homework Description', max_length=500, blank=True, null=True)
    scoring_point = models.TextField('Get score point', max_length=300, blank=True, null=True)
    re_class = models.ForeignKey('ClassList', verbose_name='Class')
    teacher = models.ForeignKey('UserProfile', verbose_name='Teacher', related_name='t_course_record')
    recorder = models.ForeignKey('UserProfile', verbose_name='Recorder', related_name='r_course_record')

    class Meta:
        unique_together = ('re_class', 'day_num')


class StudyRecord(models.Model):
    attendance = models.CharField('Attendance', choices=attendance_choice, default='checked', max_length=64)
    score = models.IntegerField('Score', choices=score_choices, default=-1)
    homework_note = models.CharField(max_length=255, verbose_name='Homework Comment', blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField('Comment', max_length=255)
    course_record = models.ForeignKey('CourseRecord', verbose_name='A Course')
    student = models.ForeignKey('Customer', verbose_name='Student')

    class Meta:
        unique_together = ('course_record', 'student')
