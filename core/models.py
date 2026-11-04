
from django.db import models
from django.core.validators import RegexValidator
import logging
import requests

from django.conf import settings


indian_phone_validator = RegexValidator(
    regex=r'^(\+91)?[6-9]\d{9}$',
    message="Enter a valid Indian mobile number with 10 digits. You may include +91."
)


class ContactMessage(models.Model):

    SERVICE_CHOICES = [
        ("Digital Marketing", "Digital Marketing"),
        ("Social Media Management", "Social Media Management"),
        ("Video Production", "Video Production"),
        ("SEO Management", "SEO Management"),
        ("Website Development", "Website Development"),
        ("Creative Design & Branding", "Creative Design & Branding"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("New", "New"),
        ("Contacted", "Contacted"),
        ("In Discussion", "In Discussion"),
        ("Converted", "Converted"),
        ("Rejected", "Rejected"),
    ]

    PRIORITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    LEAD_SOURCE_CHOICES = [
        ("Instagram", "Instagram"),
        ("Facebook", "Facebook"),
        ("Google Search", "Google Search"),
        ("Google Business Profile", "Google Business Profile"),
        ("WhatsApp", "WhatsApp"),
        ("Website", "Website"),
        ("Referral", "Referral"),
        ("Other", "Other"),
    ]

    name = models.CharField(max_length=150)

    email = models.EmailField(
        max_length=254,
        error_messages={
            "invalid": "Enter a valid email address."
        }
    )

    phone = models.CharField(
        max_length=13,
        validators=[indian_phone_validator]
    )

    service = models.CharField(
        max_length=100,
        choices=SERVICE_CHOICES,
        blank=True
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New"
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="Medium",
        verbose_name="Client Priority"
    )

    lead_source = models.CharField(
        max_length=30,
        choices=LEAD_SOURCE_CHOICES,
        default="Other",
        verbose_name="Lead Source"
    )
    
    follow_up_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Next Follow-up Date"
    )

    follow_up_notes = models.TextField(
        blank=True,
        verbose_name="Follow-up Notes"
    )

    follow_up_completed = models.BooleanField(
        default=False,
        verbose_name="Follow-up Completed"
    )


    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    @property
    def enquiry_id(self):
        return f"ENQ-{self.pk:06d}" if self.pk else "Pending"

    def save(self, *args, **kwargs):
        old_status = None

        if self.pk:
            old_status = (
                ContactMessage.objects
                .filter(pk=self.pk)
                .values_list("status", flat=True)
                .first()
            )

        super().save(*args, **kwargs)

        # Sync only when an existing enquiry's status changes
        if old_status is not None and old_status != self.status:

            webhook_url = settings.GOOGLE_SHEETS_WEBHOOK_URL

            if webhook_url:
                try:
                    response = requests.post(
                        webhook_url,
                        json={
                            "action": "update_status",
                            "enquiry_id": self.enquiry_id,
                            "status": self.status,
                        },
                        timeout=30,
                    )

                    response.raise_for_status()

                    result = response.json()

                    if result.get("status") != "success":
                        raise ValueError(
                            result.get("message", "Google Sheets update failed.")
                        )

                    logging.getLogger(__name__).info(
                        "Google Sheets status updated for %s",
                        self.enquiry_id
                    )

                except Exception:
                    logging.getLogger(__name__).exception(
                        "Google Sheets status sync failed for %s",
                        self.enquiry_id
                    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Enquiry"
        verbose_name_plural = "Contact Enquiries"

    def __str__(self):
        return f"{self.enquiry_id} - {self.name} - {self.phone}"

class FollowUpActivity(models.Model):

    CONTACT_METHOD_CHOICES = [
        ("WhatsApp", "WhatsApp"),
        ("Phone", "Phone Call"),
        ("Email", "Email"),
        ("Meeting", "Meeting"),
        ("Other", "Other"),
    ]

    enquiry = models.ForeignKey(
        ContactMessage,
        on_delete=models.CASCADE,
        related_name="activities",
        verbose_name="Client Enquiry"
    )

    contact_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Contact Date & Time"
    )

    contact_method = models.CharField(
        max_length=20,
        choices=CONTACT_METHOD_CHOICES,
        default="WhatsApp"
    )

    discussion_details = models.TextField(
        verbose_name="Discussion Details"
    )

    client_response = models.TextField(
        blank=True,
        verbose_name="Client Response"
    )

    next_follow_up_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Next Follow-up Date"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-contact_date"]
        verbose_name = "Follow-up Activity"
        verbose_name_plural = "Follow-up Activities"

    def __str__(self):
        return f"{self.enquiry.enquiry_id} - {self.contact_method}"