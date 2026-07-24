from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.db.models import Q


class DepartmentViewlist(generics.ListCreateAPIView):
    
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializser
    # permission_classes = [IsAuthenticated]

    
class DepartmentDetailView(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializser
    # permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
            
class StudentDetailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerialiser
    # permission_classes = [IsAuthenticated]
    
    
class OfferListView(generics.ListAPIView):
    serializer_class = CourseOfferingSerialiser
    # permission_classes = [IsAuthenticated]
    def get_queryset(self):
        student = self.request.user.student
        return CourseOffering.objects.filter(course__dep=student.dep)
    
class AllOfferingListView(generics.ListAPIView):
    serializer_class = CourseOfferingSerialiser
    # permission_classes = [IsAuthenticated]
    def get_queryset(self):
        courses = CourseOffering.objects.filter(course__is_active=True, sem__is_active=True)
        return courses

# class StudentListView(generics.ListAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerialiser     

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer 
        

class StudentDashboardView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def get(self,request):
        student = Student.objects.get(id=1)
        # student = request.user.student
        serializer = StudentDetailSerialiser(student)

        return Response(
            {
                "message": "Welcome",
                "student":serializer.data
            }
        )

class StudentHistory(APIView):
    # permission_classes = [IsAuthenticated]
    # serializer_class = StudentHistorySerialiser
    def get_queryset(self, request):
        # student = request.user.student.id
        student = 1
        return Enrollment.objects.filter(stu=student, status__in=["accepted", "not accepted"])
    
    def get(self, request):
        queryset = self.get_queryset(request)
        
        serializer = StudentHistorySerialiser(
            queryset,
            many=True
        )
        return Response({"data":serializer.data})
    
