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
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum

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
        self.validate_offering(student, offering)
             
        enrollment = Enrollment.objects.create(
            stu=student,
            offering=offering_id,
        )
        return Response(
            { "message": "course added", "enrollmentID": enrollment.id},
            status=status.HTTP_201_created  
        )
    
    def delete(self, request, enrollment_id):
        self.check_registraition_time()
        student = request.user.student

        enrollment = get_object_or_404(
            Enrollment,
            id=enrollment_id,
            stu=student
        )

        if enrollment.status != "temp":
            raise ValidationError(
                "Only temporary courses can be deleted."
            )

        enrollment.status = "delete"
        enrollment.save()

        return Response(
            {
                "message": "Course deleted successfully."
            },
            status=status.HTTP_200_OK
        )
        
    def put(self, request, enrollment_id):
        self.check_registraition_time()
        student = request.user.student
        
        enrollment = get_object_or_404(
            Enrollment,
            id=enrollment_id,
            stu=student
        )

        if enrollment.status != "temp":
            raise ValidationError(
                "Only temporary courses can become final."
            )

        enrollment.status = "final"
        enrollment.save()

        return Response(
            {
                "message": "Course finalized successfully."
            },
            status=status.HTTP_200_OK
        )
    
    def validate_offering(self, student, offering):
        self.check_registraition_time()
        self.validate_semester(offering)
        self.check_already_passed(student, offering)
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
        self.check_conflict(student, offering)
        self.check_prerequisite(student, offering)
        self.check_credit_limit(student, offering)
        
    def check_conflict(self, student, offering):

        new_schedules = ClassSchedule.objects.filter(
            offering=offering
        )

        new_exams = ExamSchedule.objects.filter(
            offering=offering
        )

        current_schedules = ClassSchedule.objects.filter(
            offering__enrollments__stu=student,
            offering__enrollments__status__in=["final", "temp"]
        )

        current_exams = ExamSchedule.objects.filter(
            offering__enrollments__stu=student,
            offering__enrollments__status__in=["final", "temp"]
        )

        for new_schedule in new_schedules:

            conflict = current_schedules.filter(
                day_of_week=new_schedule.day_of_week,
                start_time__lt=new_schedule.end_time,
                end_time__gt=new_schedule.start_time
            )

            if conflict.exists():
                raise ValidationError(
                    "This course has a class time conflict with another course."
                )

        for new_exam in new_exams:

            conflict = current_exams.filter(
                exam_date=new_exam.exam_date,
                start_time__lt=new_exam.end_time,
                end_time__gt=new_exam.start_time
            )

            if conflict.exists():
                raise ValidationError(
                    "This course has an exam time conflict with another course."
                )
    
    def check_prerequisite(self, student, offering):

        prerequisites = Prerequisite.objects.filter(
            course=offering.course
        )

        for prerequisite in prerequisites:

            previous_enrollment = Enrollment.objects.filter(
                stu=student,
                offering__course=prerequisite.precourse,
                status="accepted"
            ).first()

            if not previous_enrollment:
                raise ValidationError(
                    f"You must pass {prerequisite.precourse} first."
                )
                
    def validate_semester(self, offering):

        semester = offering.sem

        if not semester.is_active:
            raise ValidationError(
                "This course is not offered in the current semester."
            )
                
    def check_credit_limit(self, student, offering):

        current_credits = Enrollment.objects.filter(
            stu=student,
            offering__sem=offering.sem,
            status__in=["temp", "final"]
        ).aggregate(
            total=Sum("offering__course__credits")
        )["total"] or 0

        new_credits = offering.course.credits

        if current_credits + new_credits > settings.MAX_STUDENT_CREDITS:
            raise ValidationError(
                f"You cannot register for more than "
                f"{settings.MAX_STUDENT_CREDITS} credits."
            )
    
    def check_already_passed(self, student, offering):

        already_passed = Enrollment.objects.filter(
            stu=student,
            offering__course=offering.course,
            status="accepted"
        ).exists()

        if already_passed:
            raise ValidationError(
                "You have already passed this course."
            )
            
    def check_registraition_time(self):
        today = timezone.localdate()
        semester = Semester.objects.get(
            is_active=True
        )
        if today < semester.registration_start_date:
            raise ValidationError(
                "Registration has not started yet."
            )

        if today > semester.registration_end_date:
            raise ValidationError(
                "Registration period has ended."
            )
