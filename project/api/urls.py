from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # path('department/', views.DepartmentViewlist.as_view(), name='department_list'),
    # path('department/<int:pk>/',views.DepartmentDetailView.as_view(), name='department_detail_view'),
    # path('student/<int:pk>/',views.StudentDetailView.as_view(), name='student_view'),    
    path('login/',views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("auth/token/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('auth/refresh/',TokenRefreshView.as_view()),
    path('student/dashboard/',views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('student/history/',views.StudentHistory.as_view(), name='student_history'),
    path('registration/courses/',views.AllOfferingListView.as_view(), name='courses_list_view'),
    path('registration/list/',views.RegistrationList.as_view(), name='registration_list_view'),
    path('registration/add/<int:offering_id>/',views.StudentRegistration.as_view(), name='registration_post'),
    path('registration/final/<int:enrollment_id>/',views.StudentRegistration.as_view(), name='registration_put'),
    path('registration/delete/<int:enrollment_id>/',views.DeleteRegistraition.as_view(), name='registration_delete'),

]
