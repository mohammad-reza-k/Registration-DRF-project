from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # path('department/', views.DepartmentViewlist.as_view(), name='department_list'),
    # path('department/<int:pk>/',views.DepartmentDetailView.as_view(), name='department_detail_view'),

    # path('student/<int:pk>/',views.StudentDetailView.as_view(), name='student_view'),
    path('allofferingcourses/',views.AllOfferingListView.as_view(), name='all_available_courses'),
    
    path('login/',views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('student/dashboard/',views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('student/history/',views.StudentHistory.as_view(), name='student_history'),
    # path('student/registration/',views..as_view(), name='student_registration'),
    path('refresh/',TokenRefreshView.as_view()),

]
