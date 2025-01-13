from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

class Student(models.Model):
    DEGREE_TYPE_CHOICES = [
        ('Certificate', 'Certificate'),
        ('Diploma', 'Diploma'),
        ('Bachelor', 'Bachelor'),
        ('Master', 'Master'),
        ('PhD', 'PhD'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=True, null=True, default="test@test.com", )
    phone = models.CharField(max_length=15, blank=True, null=True, default="077123456")
    date_of_birth = models.DateField(blank=True, null=True, default="1991-10-12")
    gender = models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, default='Male')
    address = models.TextField(blank=True, null=True, default="Jaffna")
    nationality = models.CharField(max_length=100, blank=True, null=True, default="Sri Lankan")

    degree_type = models.CharField(max_length=50, choices=DEGREE_TYPE_CHOICES, default='Certificate')
    degree_provider = models.CharField(max_length=255, default='QBUK')
    degree_name = models.CharField(max_length=255, default='Diploma in Nursing Assistant Level 4')
    started_date = models.DateField()
    completed_date = models.DateField()
    awarded_date = models.DateField()
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    certificate_verification_number = models.CharField(max_length=50, unique=True)
    candidate_number = models.CharField(max_length=50, unique=True)
    batch_number = models.CharField(max_length=50, default="001")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            # Generate QR Code URL
            qr_data = f"https://mcniqbuk.co.uk/verify/{self.certificate_verification_number}"

            # Generate QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            # Create an image
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer)
            buffer.seek(0)
            self.qr_code.save(f'{self.certificate_verification_number}.png', File(buffer), save=False)
            buffer.close()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.certificate_verification_number}"
