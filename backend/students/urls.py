from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, UploadStudentsView, VerifyStudentAPIView

router = DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload-students/', UploadStudentsView.as_view(), name='upload_students'),
    path('students/verify/<str:certificateNumber>/', VerifyStudentAPIView.as_view(), name='verify-student'),
]
