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
    
    class Meta:
        model = Student
        fields = "__all__"
        
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
        model = Student
        fields = "__all__"
class StudentSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = "__all__"
class StudentSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = "__all__"
class StudentSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = "__all__"
class StudentSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = "__all__"
