from .models import *
from .serializer import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404

class DepartmentViewlist(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializser
    permission_classes = [IsAuthenticated]

    
class DepartmentDetailView(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializser
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
            
class StudentDetailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerialiser
    permission_classes = [IsAuthenticated]
    
    
class OfferListView(generics.ListAPIView):
    serializer_class = CourseOfferingSerialiser
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        student = self.request.user.student
        return CourseOffering.objects.filter(course__dep=student.dep)
    
class AllOfferingListView(generics.ListAPIView):
    serializer_class = CourseOfferingSerialiser
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        courses = CourseOffering.objects.filter(course__is_active=True, sem__is_active=True)
        return courses     

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer 
        

class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        # student = Student.objects.get(id=1)
        student = request.user.student
        serializer = StudentDetailSerialiser(student)

        return Response(
            {
                "message": "Welcome",
                "student":serializer.data
            }
        )

class StudentHistory(APIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = StudentHistorySerialiser
    def get_queryset(self, request):
        student = request.user.student.id
        # student = 1
        return Enrollment.objects.filter(stu=student, status__in=["accepted", "not accepted"])
    
    def get(self, request):
        queryset = self.get_queryset(request)
        
        serializer = StudentHistorySerialiser(
            queryset,
            many=True
        )
        return Response({"data":serializer.data})
    
class StudentRegistration(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        student = request.user.student
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        offering_id = serializer.validated_data["offering_id"]
        offering = get_object_or_404(
            CourseOffering,
            id=offering_id
        )
        self.validate_offering(offering)
        
        already_enrolled = Enrollment.objects.filter(
            stu=student,
            offering=offering,
            status__in=["accepted", "not accepted","temp"]
        ).exists()
        if already_enrolled:
             return Response(
                {"error": "You are already enrolled in this course."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        enrollment = Enrollment.objects.create(
            stu=student,
            offering=offering_id,
        )
        return Response(
            { "message": "course added", "enrollmentID": enrollment.id},
            status=status.HTTP_201_created  
        )
    
    def validate_offering(self, offering):

        if not offering.course.is_active:
            raise ValidationError(
                "This course is not active."
            )

        if offering.registered_count >= offering.capacity:
            raise ValidationError(
                "This course is full."
            )

        if offering.status != "can":
            raise ValidationError(
                "This course is not available for registration."
            )            

