from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class DepartmentSerializser(serializers.ModelSerializer):
    def validate(self, data):
        department_name = data.get('department_name')
        if not data.get('faculty_name'):
            data['faculty_name'] = department_name
            
        return data
    
    class Meta:
        model = Department
        fields = "__all__"
        

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['is_student'] = user.is_student
        token['is_professor'] = user.is_professor

        return token

class StudentSerialiser(serializers.ModelSerializer):
    phone_numbers = serializers.SerializerMethodField()
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
    
class CourseOfferSerialiser(serializers.ModelSerializer):
    class Meta:
        model = CourseOffering
        fields = "__all__"
        
class ProfessorSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Professor
        fields = "__all__"
        
class CourseSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = "__all__"
        
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

class SemesterSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Semester
        fields = "__all__"
        
class PrerequisiteSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Prerequisite
        fields = "__all__"
        
    
