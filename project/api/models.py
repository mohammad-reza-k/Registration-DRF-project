from django.db import models
from django.db.models import Q, CheckConstraint, F, UniqueConstraint
from django.contrib.auth.models import AbstractUser
from django.db import models    

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)
    
class Department(models.Model):
    # id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=50, unique=True)
    faculty_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.department_name


class DepartmentPhone(models.Model):
    # id = models.AutoField(primary_key=True)
    dep = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE 
    )
    phone_number = models.CharField(unique=True, max_length=11)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['dep', 'phone_number'], name='unique_department_phone')
        ]

    def __str__(self):
        return f"{self.dep} - {self.phone_number}"


class Professor(models.Model):
    # id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    GENDER_CHOICES = [
            ('M', 'Male'),
            ('F', 'Female'),
        ]
    
    ACHADEMIC_CHOICES = [('TA','ta'),('professor','Professor')]

    gender = models.CharField(max_length=5,choices=GENDER_CHOICES)
    academic_rank = models.CharField(max_length=20, blank=True, null=True,choices=ACHADEMIC_CHOICES)
    national_code = models.CharField(unique=True, max_length=10)
    date_of_birth = models.DateField(blank=True, null=True)
    dep = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE
    )
    # class Meta:

    #     constraints = [
    #         CheckConstraint(
    #             condition=Q(academic_rank__in=['TA','ta','professor']),
    #             name="professor_academic_rank_check"
    #         )
    #     ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ProfessorEmail(models.Model):
    # id = models.AutoField(primary_key=True)
    prof = models.ForeignKey(
        Professor, 
        on_delete=models.CASCADE
    )
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)


    def __str__(self):
        return self.email or "No Email"


class ProfessorPhone(models.Model):
    # id = models.AutoField(primary_key=True)
    prof = models.ForeignKey(
        Professor, 
        on_delete=models.CASCADE
    )
    phone_number = models.CharField(unique=True, max_length=11)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['prof', 'phone_number'], name='unique_professor_phone')
        ]

    def __str__(self):
        return self.phone_number


class Semester(models.Model):
    # id = models.AutoField(primary_key=True)
    term_name = models.CharField(unique=True, max_length=20)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    registration_start_date = models.DateField(blank=True, null=True)
    registration_end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        constraints = [
            CheckConstraint(
                condition=Q(registration_start_date__lt=F('registration_end_date')), name='semester_registration_check'
            ),
            CheckConstraint(
                condition=Q(start_date__lt=F('end_date')), name='semester_date_check'
            )
        ]

    def __str__(self):
        return self.term_name


class Student(models.Model):
    # id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    student_number = models.CharField(unique=True, max_length=10)
    national_code = models.CharField(unique=True, max_length=10)
    date_of_birth = models.DateField(blank=True, null=True)
    entry_year = models.IntegerField(blank=True, null=True)
    dep = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            CheckConstraint(condition=Q(entry_year__gte=1398), name="student_entry_year_check")
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_number})"


class StudentEmail(models.Model):
    # id = models.AutoField(primary_key=True)
    stu = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE
    )
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)


    def __str__(self):
        return self.email or "No Email"


class StudentPhone(models.Model):
    # id = models.AutoField(primary_key=True)
    stu = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE
    )
    phone_number = models.CharField(unique=True, max_length=11)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['stu', 'phone_number'], name='unique_student_phone')
        ]

    def __str__(self):
        return self.phone_number


class Course(models.Model):
    # id = models.AutoField(primary_key=True)
    course_code = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    COURSE_TYPE_CHOICES = [
        ('professional', 'Professional'),
        ('base', 'Base'),
        ('lab', 'Laboratory'),
        ('public', 'Public'),
    ]
    course_type = models.CharField(max_length=20,choices=COURSE_TYPE_CHOICES)
    credits = models.IntegerField()
    is_active = models.BooleanField(default=True)
    dep = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            # CheckConstraint(
            #     condition=Q(course_type__in=['profetional', 'base', 'lab', 'public']), name='course_type_check'
            # ),
            CheckConstraint(condition=Q(credits__range=(0, 4)), name="course_credits_check")
        ]

    def __str__(self):
        return f"{self.course_code} - {self.name}"


class CourseOffering(models.Model):
    # id = models.AutoField(primary_key=True)
    STATUS_CHOICES = [
        ('can', "Can"),
        ('cant', "Can't"),
    ]
    status = models.CharField(max_length=20, default='can',choices=STATUS_CHOICES)
    capacity = models.IntegerField(blank=True, null=True, default=30)
    registered_count = models.IntegerField(blank=True, null=True, default=0)
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE
    )
    prof = models.ForeignKey(
        Professor, 
        on_delete=models.CASCADE
    )
    sem = models.ForeignKey(
        Semester, 
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['course', 'prof', 'sem'], name='unique_offering'),
            # CheckConstraint(
            #     condition=Q(status__in=['can','cant']),name='offering_status_check'
            # ),
            CheckConstraint(
                condition=Q(registered_count__lte=F('capacity')),name='offering_capacity_check'
            )
        ]

    def __str__(self):
        return f"{self.course} - {self.prof} - {self.sem}"


class Enrollment(models.Model):
    # id = models.AutoField(primary_key=True)
    enrollment_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    STATUS_CHOICES = [
    ('accepted', 'Accepted'),
    ('final', 'Final'),
    ('temp', 'Temporary'),
    ('delete', 'Deleted'),
    ('not_accepted', 'Not Accepted'),
    ]
    status = models.CharField(max_length=20, blank=True, null=True, default='temp',choices=STATUS_CHOICES)
    offering = models.ForeignKey(
        CourseOffering, 
        on_delete=models.CASCADE
    )
    stu = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['stu', 'offering'], name='unique_enrollment'),
            # CheckConstraint(
            #     condition=Q(status__in=['accepted','final','temp','delete','not accepted']), name='enrollment_status_check'
            # )
        ]

    def __str__(self):
        return f"{self.stu} - {self.offering}"


class ExamSchedule(models.Model):
    # id = models.AutoField(primary_key=True)
    room_number = models.IntegerField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    exam_date = models.DateField(blank=True, null=True)
    offering = models.ForeignKey(
        CourseOffering, 
        on_delete=models.CASCADE
    )
    dep = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['room_number', 'start_time', 'exam_date'], name='unique_exam_schedule'),
            CheckConstraint(condition=Q(start_time__lt=F('end_time')), name='exam_time_check'),
        ]

    def __str__(self):
        return f"Exam {self.offering} - Room {self.room_number}"


class ClassSchedule(models.Model):
    # id = models.AutoField(primary_key=True)
    room_number = models.IntegerField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    DOW_CHOICES = [
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
    ]
    day_of_week = models.CharField(max_length=20, blank=True, null=True,choices=DOW_CHOICES)
    offering = models.ForeignKey(
        CourseOffering, 
        on_delete=models.CASCADE
    )
    dep = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['room_number', 'start_time', 'day_of_week'], name='unique_class_schedule'),
            CheckConstraint(condition=Q(start_time__lt=F('end_time')), name='class_time_check'),
            # CheckConstraint(
            #     condition=Q(day_of_week__in=['sat','sun','mon','tue','wed','fri']),name='class_dow_check'
            # ),
        ]

    def __str__(self):
        return f"Class {self.offering} - {self.day_of_week} {self.start_time}"


class Grade(models.Model):
    # id = models.AutoField(primary_key=True)
    GRADE_TYPE_CHOICES = [
    ('midterm', 'Midterm'),
    ('quiz', 'Quiz'),
    ('final', 'Final'),
    ('lastterm', 'Last Term'),
    ('homework', 'Homework'),
    ]
    grade_type = models.CharField(max_length=30,choices=GRADE_TYPE_CHOICES)
    numeric_grade = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    grade_date = models.DateField(auto_now_add=True, blank=True, null=True)
    prof = models.ForeignKey(
        Professor, 
        on_delete=models.CASCADE
    )
    enroll = models.ForeignKey(
        Enrollment,on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['enroll', 'grade_type'], name='unique_grade'),
            # CheckConstraint(
            #     condition=Q(grade_type__in=['midterm','queez','final','lastterm','homework']), name='grade_type_check'
            # ),
            CheckConstraint(
                condition=Q(numeric_grade__gte=0.00) & Q(numeric_grade__lte=20.00),name='grade_number_check'
            )
        ]

    def __str__(self):
        return f"{self.enroll} - {self.grade_type}: {self.numeric_grade}"


class Prerequisite(models.Model):
    # id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='main_course'
    )
    precourse = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='pre_course'
    )
    min_grade = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True,default=10.00)
    PRETYPE_CHOICES = [('pre','Pre'),('together','Together')]
    pre_type = models.CharField(max_length=20, blank=True, null=True,choices=PRETYPE_CHOICES)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['course', 'precourse'], name='unique_prerequisite'),
            # CheckConstraint(
            #     condition=Q(pre_type__in=['pre','together']), name='prerequisite_type_check'
            # )
        ]

    def __str__(self):
        return f"{self.course} needs {self.precourse}"