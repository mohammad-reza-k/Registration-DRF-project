from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "is_student",
        "is_professor",
        "is_staff",
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            "Roles",
            {
                "fields": (
                    "is_student",
                    "is_professor",
                )
            },
        ),
    )
    list_filter = ["is_student","is_professor","is_staff"]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ["department_name", "faculty_name"]
    list_filter = ["faculty_name"]
    list_display = ["id", "faculty_name", "department_name"]
    
@admin.register(DepartmentPhone)
class DepartmentPhoneAdmin(admin.ModelAdmin):
    search_fields = ["phone_number", "dep"]
    list_filter = ["dep"]
    list_display = ["dep", "phone_number"]
    
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    search_fields = ["term_name"]
    list_filter = ["is_active"]
    list_display = ["id","term_name","start_date","end_date", "is_active"]
    
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ["first_name","last_name","student_number","dep"]
    list_filter = ["gender","entry_year","dep"]
    list_display = ["id","first_name","last_name","student_number","national_code","entry_year","dep"]
    
@admin.register(StudentEmail)
class StudentEmailAdmin(admin.ModelAdmin):
    search_fields = ["stu","email"]
    list_filter = ["stu"]
    list_display = ["stu","email"]
    
@admin.register(StudentPhone)
class StudentPhoneAdmin(admin.ModelAdmin):
    search_fields = ["stu","phone_number"]
    list_filter = ["stu"]
    list_display = ["stu","phone_number"]

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    search_fields = ["first_name","last_name","academic_rank","dep"]
    list_filter = ["dep"]
    list_display = ["id","first_name","last_name","academic_rank","national_code","dep"]

@admin.register(ProfessorEmail)
class ProfessorEmailAdmin(admin.ModelAdmin):
    search_fields = ["prof","email"]
    list_filter = ["prof"]
    list_display = ["prof","email"]

@admin.register(ProfessorPhone)
class ProfessorPhoneAdmin(admin.ModelAdmin):
    search_fields = ["prof","phone_number"]
    list_filter = ["prof"]
    list_display = ["prof","phone_number"]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ["name","dpe","course_type","course_code"]
    list_filter = ["dep","is_active"]
    list_display = ["id","name","credits","course_type","is_active","course_code","dep"]

@admin.register(CourseOffering)
class COfferingAdmin(admin.ModelAdmin):
    search_fields = ["course","prof","sem","status"]
    list_filter = ["sem"]
    list_display = ["id","course","prof","sem","capacity","registered_count","status"]

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    search_fields = ["offering","stu","status"]
    list_display = ["id","offering","stu","status","enrollment_date"]

@admin.register(ClassSchedule)
class CScheduleAdmin(admin.ModelAdmin):
    search_fields = ["offering","dep""day_of_week"]
    list_filter = ["dep"]
    list_display = ["id","offering","dep","start_time","end_time","day_of_week","room_number"]

@admin.register(ExamSchedule)
class EScheduleAdmin(admin.ModelAdmin):
    search_fields = ["offering","dep","start_time","exam_date","room_number"]
    list_filter = ["dep"]
    list_display = ["id","offering","dep","start_time","end_time","exam_date","room_number"]

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    search_fields = ["enroll","prof","grade_type"]
    list_filter = ["grade_type"]
    list_display = ["id","enroll","prof","grade_type","numeric_grade"]

@admin.register(Prerequisite)
class StudentEmailAdmin(admin.ModelAdmin):
    search_fields = ["course","precourse"]
    list_filter = ["course","precourse"]
    list_display = ["course","precourse","pre_type"]
