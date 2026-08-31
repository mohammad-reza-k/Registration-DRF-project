from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['is_student'] = user.is_student
        token['is_professor'] = user.is_professor

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_student:
            raise AuthenticationFailed(
                "Only students can login here.")
        
        data["is_student"] = self.user.is_student
        data["is_professor"] = self.user.is_professor
        return data

class DepartmentSerializser(serializers.ModelSerializer):
    def validate(self, data):
        department_name = data.get('department_name')
        if not data.get('faculty_name'):
            data['faculty_name'] = department_name
            
        return data
    
    class Meta:
        model = Department
        fields = ["faculty_name"]
        

class StudentDetailSerialiser(serializers.ModelSerializer):
    phone_numbers = serializers.SerializerMethodField()
    dep = DepartmentSerializser(read_only=True)
    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "gender", 
            "student_number", 
            "national_code", 
            "date_of_birth", 
            "entry_year", 
            "dep",
            "phone_numbers" 
            ]
        
        
    def get_phone_numbers(self,obj):
        phone = StudentPhone.objects.filter(stu=obj).all()
        return [p.phone_number for p in phone] if phone else None

class SemesterSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Semester
        fields = ["term_name","start_date","end_date","is_active"]

class ProfessorSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ["first_name","last_name"]
        
class CourseSerialiser(serializers.ModelSerializer):
    dep = DepartmentSerializser(read_only=True)
    class Meta:
        model = Course
        fields = ["name", "description", "course_type", "credits", "is_active","dep"]

class CourseOfferingSerialiser(serializers.ModelSerializer):
    course = CourseSerialiser(read_only=True)
    sem = SemesterSerialiser(read_only=True)
    prof = ProfessorSerialiser(read_only=True)
    class Meta:
        model = CourseOffering
        fields = "__all__"

      
class StudentHistorySerialiser(serializers.ModelSerializer):
    course_name = serializers.CharField(source="offering.course.name",read_only=True)
    credits = serializers.IntegerField(source="offering.course.credits",read_only=True)
    semester = serializers.CharField(source="offering.sem.term_name",read_only=True)
    professor_first_name = serializers.CharField(source="offering.prof.first_name",read_only=True)
    professor_last_name = serializers.CharField(source="offering.prof.last_name",read_only=True)
    class Meta:
        model = Enrollment
        fields = [
            "enrollment_date",
            "status",
            "course_name",
            "credits",
            "semester",
            "professor_first_name",
            "professor_last_name",
            "stu"
            ]

class RegistrationSerializer(serializers.Serializer):
    offering_id = serializers.IntegerField()
    
class ClassSerialiser(serializers.ModelSerializer):
    class Meta:
        model = ClassSchedule
        fields = "__all__"
        
class ExamSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = ExamSchedule
        fields = "__all__"
        
class GradeSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Grade
        fields = "__all__"
        
class EnrollmentSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Enrollment
        fields = "__all__"

        
class PrerequisiteSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Prerequisite
        fields = "__all__"
        
    