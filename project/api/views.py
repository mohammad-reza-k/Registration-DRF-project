from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics

class DepartmentViewlist(generics.ListCreateAPIView):
    
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializser
    permission_classes = [IsAuthenticated]

    
class DepartmentDetailView(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializser
    # permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer         
        
class StudentDetailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerialiser
    # permission_classes = [IsAuthenticated]
    
    
class OfferListView(generics.ListAPIView):
    serializer_class = CourseOfferSerialiser
    # permission_classes = [IsAuthenticated]
    def get_queryset(self):
        student = self.request.user.student
        return CourseOffering.objects.filter(course__dep=student.dep)

# class StudentListView(generics.ListAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerialiser     

    
    
