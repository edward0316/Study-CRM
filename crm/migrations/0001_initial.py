# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2020-05-09 07:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Campus')),
                ('address', models.CharField(blank=True, max_length=512, null=True, verbose_name='Address Details')),
            ],
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(choices=[('Linux', 'Senior/Midium Level Linux'), ('Python Fullstack', 'Senior Python Fullstack')], max_length=64, verbose_name='Course Name')),
                ('semester', models.IntegerField(verbose_name='Semester')),
                ('price', models.IntegerField(default=10000, verbose_name='Tuition')),
                ('memo', models.CharField(blank=True, max_length=100, null=True, verbose_name='Introduction')),
                ('start_date', models.DateField(verbose_name='Commencement date')),
                ('graduate_date', models.DateField(blank=True, null=True, verbose_name='Graduate date')),
                ('class_type', models.CharField(blank=True, choices=[('fulltime', 'fulltime class'), ('online', 'online class'), ('weekend', 'weekend class')], max_length=64, null=True)),
                ('campuses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Campus', verbose_name='Campus')),
            ],
        ),
        migrations.CreateModel(
            name='ConsultRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(verbose_name='Chatting history')),
                ('status', models.CharField(choices=[('A', 'No study plan recently'), ('B', 'Enroll in 1 month'), ('C', 'Enroll in 2 months'), ('D', 'Enroll in 1 week'), ('E', 'Paid deposit'), ('F', 'Enrolled'), ('G', 'Full Paid'), ('H', 'Error')], help_text="Select the customer's status", max_length=8, verbose_name='Customer Status')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='The last chat date')),
                ('delete_status', models.BooleanField(default=False, verbose_name='Delete Status')),
            ],
        ),
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_num', models.IntegerField(help_text='Input a integer to show which class is it', verbose_name='Class Order')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Class date')),
                ('course_title', models.CharField(blank=True, max_length=64, null=True, verbose_name='Course Title')),
                ('course_memo', models.TextField(blank=True, max_length=300, null=True, verbose_name='Course content')),
                ('has_homework', models.BooleanField(default=True, verbose_name='has homework')),
                ('homework_title', models.CharField(blank=True, max_length=64, null=True, verbose_name='Homework Title')),
                ('homework_memo', models.TextField(blank=True, max_length=500, null=True, verbose_name='Homework Description')),
                ('scoring_point', models.TextField(blank=True, max_length=300, null=True, verbose_name='Get score point')),
                ('re_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.ClassList', verbose_name='Class')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qq', models.CharField(blank=True, help_text='QQ Number must be unique', max_length=64, null=True, verbose_name='QQ')),
                ('qq_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='QQ name')),
                ('name', models.CharField(blank=True, help_text='Student should use their real name after enrolled a course', max_length=32, null=True, verbose_name='Name')),
                ('sex', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=16, null=True, verbose_name='Gender')),
                ('birthday', models.DateField(blank=True, default=None, help_text='Format yyyy-mm-dd', null=True, verbose_name='D.O.B')),
                ('phone', models.BigIntegerField(blank=True, null=True, verbose_name='Phone Number')),
                ('source', models.CharField(choices=[('qq', 'qq group'), ('referral', 'Intruduced by friend'), ('website', 'official website'), ('baidu_ads', 'baidu campaign'), ('office_direct', 'office enroll'), ('WoM', 'Koubei Software'), ('public_class', 'public class'), ('website_luffy', 'Luffy Website'), ('others', 'others')], default='qq', max_length=64, verbose_name='Customer source statistic')),
                ('course', multiselectfield.db.fields.MultiSelectField(choices=[('Linux', 'Senior/Midium Level Linux'), ('Python Fullstack', 'Senior Python Fullstack')], max_length=22, verbose_name='Consulting Courses')),
                ('class_type', models.CharField(choices=[('fulltime', 'fulltime class'), ('online', 'online class'), ('weekend', 'weekend class')], default='fulltime', max_length=64, verbose_name='Class Type')),
                ('customer_note', models.TextField(blank=True, null=True, verbose_name='Customer Note')),
                ('status', models.CharField(choices=[('signed', 'Enrolled'), ('unregistered', 'Unenrolled'), ('studying', 'styding'), ('paid_in_full', 'Paid Tuition')], default='unregistered', help_text='Current customer status', max_length=64, verbose_name='Status')),
                ('last_consult_date', models.DateField(auto_now_add=True, verbose_name='The last contact date')),
                ('next_date', models.DateField(blank=True, null=True, verbose_name='Expected next contact date')),
                ('class_list', models.ManyToManyField(to='crm.ClassList', verbose_name='Enrolled class')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Department Name')),
                ('count', models.IntegerField(default=0, verbose_name='Number of Staffs')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('why_us', models.TextField(blank=True, default=None, max_length=1024, null=True, verbose_name='Why chose us')),
                ('your_expectation', models.TextField(blank=True, max_length=1024, null=True, verbose_name='Achievement expectation')),
                ('contract_agree', models.BooleanField(default=False, verbose_name='I have read the contract and agreed its context')),
                ('contract_approved', models.BooleanField(help_text="Check the selection after veryfied student's information", verbose_name='Audited')),
                ('enrolled_date', models.DateTimeField(auto_now_add=True, verbose_name='Enrollment date')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('delete_status', models.BooleanField(default=False, verbose_name='Delete status')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='Customer name')),
                ('enrolment_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.ClassList', verbose_name='Enrolled class')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Campus')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_type', models.CharField(choices=[('deposit', 'Deposit'), ('tuition', 'Tuition'), ('transfer', 'Transfer Class Fee'), ('dropout', 'Withdraw Class'), ('refund', 'Refund')], default='deposit', max_length=64, verbose_name='Payment Method')),
                ('paid_fee', models.IntegerField(default=0, verbose_name='Paid Amount')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Note')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Payment date')),
                ('course', models.CharField(blank=True, choices=[('Linux', 'Senior/Midium Level Linux'), ('Python Fullstack', 'Senior Python Fullstack')], default='N/A', max_length=64, null=True, verbose_name='Course Name')),
                ('class_type', models.CharField(blank=True, choices=[('fulltime', 'fulltime class'), ('online', 'online class'), ('weekend', 'weekend class')], default='N/A', max_length=64, null=True, verbose_name='Class Type')),
                ('delete_status', models.BooleanField(default=False, verbose_name='Delete Status')),
                ('status', models.IntegerField(choices=[(1, 'unaudited'), (2, 'audited')], default=1, verbose_name='Audit')),
                ('confirm_date', models.DateTimeField(blank=True, null=True, verbose_name='Confirm date')),
            ],
        ),
        migrations.CreateModel(
            name='StudyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.CharField(choices=[('checked', 'In Class'), ('vacate', 'Asked Leave'), ('late', 'late'), ('absence', 'Absence'), ('leave_early', 'Leave Early')], default='checked', max_length=64, verbose_name='Attendance')),
                ('score', models.IntegerField(choices=[(100, 'A+'), (90, 'A'), (85, 'B+'), (80, 'B'), (70, 'B-'), (60, 'c+'), (50, 'c'), (40, 'c-'), (0, 'D'), (-1, 'N/A'), (-100, 'Copy'), (-1000, 'Fail')], default=-1, verbose_name='Score')),
                ('homework_note', models.CharField(blank=True, max_length=255, null=True, verbose_name='Homework Comment')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('note', models.CharField(max_length=255, verbose_name='Comment')),
                ('course_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.CourseRecord', verbose_name='A Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='Student')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.EmailField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=32, verbose_name='Name')),
                ('mobile', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='Mobile')),
                ('memo', models.TextField(blank=True, default=None, null=True, verbose_name='Comment')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('department', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Department')),
            ],
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='confirm_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='confirms', to='crm.UserProfile', verbose_name='Confirmed by whom'),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='consultant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.UserProfile', verbose_name='Sales'),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='Customer'),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='enrolment_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.ClassList', verbose_name='Enrolled Class'),
        ),
        migrations.AddField(
            model_name='customer',
            name='consultant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='crm.UserProfile', verbose_name='Sales'),
        ),
        migrations.AddField(
            model_name='customer',
            name='introduce_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='Introduced by other students'),
        ),
        migrations.AddField(
            model_name='courserecord',
            name='recorder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.UserProfile', verbose_name='Recorder'),
        ),
        migrations.AddField(
            model_name='courserecord',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Teacher', to='crm.UserProfile', verbose_name='Teacher'),
        ),
        migrations.AddField(
            model_name='consultrecord',
            name='consultant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='crm.UserProfile', verbose_name='Consultant'),
        ),
        migrations.AddField(
            model_name='consultrecord',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='Served Customer'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='teachers',
            field=models.ManyToManyField(to='crm.UserProfile', verbose_name='Teacher'),
        ),
        migrations.AlterUniqueTogether(
            name='studyrecord',
            unique_together=set([('course_record', 'student')]),
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together=set([('enrolment_class', 'customer')]),
        ),
        migrations.AlterUniqueTogether(
            name='courserecord',
            unique_together=set([('re_class', 'day_num')]),
        ),
        migrations.AlterUniqueTogether(
            name='classlist',
            unique_together=set([('course', 'semester', 'campuses')]),
        ),
    ]