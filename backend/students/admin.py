from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'degree_type', 'degree_provider', 'degree_name', 'certificate_verification_number')
    search_fields = ('first_name', 'last_name', 'certificate_verification_number', 'candidate_number')
    list_filter = ('degree_type', 'degree_provider')
