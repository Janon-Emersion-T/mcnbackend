from rest_framework.viewsets import ModelViewSet
from .models import Student
from .serializers import StudentSerializer
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

@method_decorator(csrf_exempt, name='dispatch')
class UploadStudentsView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file or not file.name.endswith('.csv'):
            return JsonResponse({'error': 'Please upload a valid CSV file.'}, status=400)

        try:
            # Read the CSV file
            data = pd.read_csv(file)

            # Validate required columns
            required_columns = ['name', 'email', 'age', 'class']  # Replace with your model fields
            if not all(col in data.columns for col in required_columns):
                return JsonResponse({'error': 'CSV file must contain the required columns: name, email, age, class'}, status=400)

            # Create Student objects
            students = [
                Student(
                    name=row['name'],
                    email=row['email'],
                    age=row['age'],
                    student_class=row['class']  # Replace 'class' with the actual field name
                )
                for _, row in data.iterrows()
            ]

            # Bulk create students
            Student.objects.bulk_create(students)
            return JsonResponse({'message': 'Students added successfully.'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class VerifyStudentAPIView(APIView):
    def get(self, request, certificateNumber):
        try:
            student = Student.objects.get(certificate_verification_number=certificateNumber)
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response(
                {"error": "Certificate not found or invalid."},
                status=status.HTTP_404_NOT_FOUND
            )