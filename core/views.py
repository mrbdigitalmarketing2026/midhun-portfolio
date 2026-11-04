
import re
import logging
import requests

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags, escape
from django.conf import settings

from .models import ContactMessage
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


def home(request):
    form_data = {}
    form_errors = {}

    if request.method == "POST":
        form_data = {
            "name": request.POST.get("name", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "phone": request.POST.get("phone", "").strip(),
            "service": request.POST.get("service", "").strip(),
            "message": request.POST.get("message", "").strip(),
        }

        phone = form_data["phone"].replace(" ", "").replace("-", "")

        if not form_data["name"]:
            form_errors["name"] = "Please enter your name."

        if not form_data["email"]:
            form_errors["email"] = "Please enter your email."

        if not phone:
            form_errors["phone"] = "Please enter your phone number."
        elif not re.fullmatch(r"(\+91)?[6-9]\d{9}", phone):
            form_errors["phone"] = "Enter a valid Indian mobile number."

        if not form_data["message"]:
            form_errors["message"] = "Please enter your project details."

        if form_data["service"] and form_data["service"] not in dict(ContactMessage.SERVICE_CHOICES):
            form_errors["service"] = "Please select a valid service."

        if not form_errors:
            enquiry = ContactMessage(
                name=form_data["name"],
                email=form_data["email"],
                phone=phone,
                service=form_data["service"],
                message=strip_tags(form_data["message"]),
            )

            try:
                # Validate all model fields, including email and phone.
                enquiry.full_clean()
                enquiry.save()

                # Send the saved enquiry to Google Sheets.
                webhook_url = settings.GOOGLE_SHEETS_WEBHOOK_URL

                if webhook_url:
                    payload = {
                        "enquiry_id": enquiry.enquiry_id,
                        "name": enquiry.name,
                        "email": enquiry.email,
                        "phone": enquiry.phone,
                        "service": enquiry.service,
                        "message": enquiry.message,
                        "status": enquiry.status,
                    }

                    try:
                        
                        response = requests.post(
                            webhook_url,
                            json=payload,
                            timeout=30,
                            allow_redirects=True,
                        )

                        logger.info("Google Sheets HTTP status: %s", response.status_code)
                        logger.info("Google Sheets response: %s", response.text[:1000])

                        response.raise_for_status()

                        result = response.json()

                        if result.get("status") != "success":
                            raise ValueError(
                                result.get("message", "Google Sheets rejected the enquiry.")
                            )


                        if result.get("status") != "success":
                            raise ValueError(
                                result.get("message", "Google Sheets rejected the enquiry.")
                            )

                        messages.success(
                            request,
                            "Thank you! Your enquiry has been submitted successfully."
                        )

                    except (requests.RequestException, ValueError) as error:
                        logger.exception("Google Sheets submission failed: %s", error)
                        messages.warning(
                            request,
                            "Your enquiry was saved, but Google Sheets could not be updated. Please try again later."
                        )
                else:
                    messages.warning(
                        request,
                        "Your enquiry was saved, but Google Sheets is not configured."
                    )
                
                
                # Send premium HTML email notification
                try:
                    subject = f"New Portfolio Enquiry - {enquiry.name}"

                    name_html = escape(enquiry.name)
                    email_html = escape(enquiry.email)
                    phone_html = escape(enquiry.phone)
                    service_html = escape(enquiry.service or "Not specified")
                    message_html = escape(enquiry.message).replace("\n", "<br>")

                    submitted_at = enquiry.created_at.strftime("%d %B %Y, %I:%M %p")

                    email_body = f"""
                New Portfolio Enquiry

                Name: {enquiry.name}
                Email: {enquiry.email}
                Phone: {enquiry.phone}
                Service: {enquiry.service or "Not specified"}

                Project Details:
                {enquiry.message}

                Submitted: {submitted_at}
                """

                    html_content = f"""
                    <div style="background:#100d18;padding:35px 15px;font-family:Arial,sans-serif;">
                    <div style="max-width:600px;margin:auto;background:#1b1725;border-radius:16px;overflow:hidden;border:1px solid #392b50;">

                        <div style="background:linear-gradient(135deg,#32145c,#7027a8);padding:30px;text-align:center;">
                        <h1 style="color:#ffffff;margin:0;font-size:27px;">MIDHUN PORTFOLIO</h1>
                        <p style="color:#e4d2ff;margin:10px 0 0;">New Client Enquiry</p>
                        </div>

                        <div style="padding:30px;color:#ffffff;">
                        <h2 style="font-size:21px;margin-top:0;">You have received a new enquiry!</h2>
                        <p style="color:#c5bdd2;font-size:14px;line-height:1.6;">
                            Someone has contacted you through your portfolio website.
                            Here are the enquiry details.
                        </p>

                        <div style="background:#272032;border-radius:10px;padding:20px;margin-top:22px;">
                            <p style="color:#b995ed;font-size:12px;margin:0 0 6px;">CLIENT NAME</p>
                            <p style="color:#ffffff;font-size:17px;margin:0 0 18px;">{name_html}</p>

                            <p style="color:#b995ed;font-size:12px;margin:0 0 6px;">EMAIL ADDRESS</p>
                            <p style="margin:0 0 18px;">
                            <a href="mailto:{email_html}" style="color:#d0a9ff;">{email_html}</a>
                            </p>

                            <p style="color:#b995ed;font-size:12px;margin:0 0 6px;">PHONE NUMBER</p>
                            <p style="color:#ffffff;margin:0 0 18px;">{phone_html}</p>

                            <p style="color:#b995ed;font-size:12px;margin:0 0 6px;">SERVICE INTERESTED IN</p>
                            <p style="color:#ffffff;margin:0;">{service_html}</p>
                        </div>

                        <h3 style="color:#d0a9ff;margin-top:28px;">Project Details</h3>
                        <div style="background:#272032;padding:18px;border-radius:10px;color:#e8e1ef;line-height:1.7;">
                            {message_html}
                        </div>

                        <p style="color:#aaa0b8;font-size:12px;margin-top:24px;">
                            Submitted on: {submitted_at}
                        </p>

                        <div style="text-align:center;margin-top:28px;">
                            <a href="mailto:{email_html}?subject=Regarding%20your%20portfolio%20enquiry"
                            style="display:inline-block;background:#8139c5;color:#ffffff;text-decoration:none;padding:14px 26px;border-radius:8px;font-weight:bold;">
                            Reply to Client
                            </a>
                        </div>
                        </div>

                        <div style="background:#15111d;padding:20px;text-align:center;">
                        <p style="color:#a99db7;font-size:12px;margin:0;">
                            Midhun Portfolio | Digital Marketer & Creative Professional
                        </p>
                        </div>

                    </div>
                    </div>
                    """

                    email = EmailMultiAlternatives(
                        subject=subject,
                        body=email_body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[settings.ENQUIRY_NOTIFICATION_EMAIL],
                        reply_to=[enquiry.email],
                    )

                    email.attach_alternative(html_content, "text/html")
                    email.send(fail_silently=False)

                    logger.info("Premium HTML enquiry notification sent successfully.")

                except Exception as error:
                    logger.exception("Email notification failed: %s", error)
                    messages.warning(
                        request,
                        "Your enquiry was saved, but the email notification could not be sent."
                    )

                return redirect("home")

            except ValidationError as error:
                for field, errors in error.message_dict.items():
                    form_errors[field] = errors[0]

    return render(
        request,
        "home.html",
        {
            "form_data": form_data,
            "form_errors": form_errors,
        }
    )
