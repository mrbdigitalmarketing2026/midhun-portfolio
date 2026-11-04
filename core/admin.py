
from django.contrib import admin
from .models import ContactMessage, FollowUpActivity
from django.utils.html import format_html
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import date
from django.utils import timezone

class FollowUpActivityInline(admin.TabularInline):

    model = FollowUpActivity
    extra = 1

    fields = (
        "contact_date",
        "contact_method",
        "discussion_details",
        "client_response",
        "next_follow_up_date",
    )

    readonly_fields = ("contact_date",)

    ordering = ("-contact_date",)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    inlines = [FollowUpActivityInline]

    list_display = (
        "enquiry_id",
        "name",
        "phone",
        "email",
        "service",
        "status",
        "priority",
        "lead_source",
        "follow_up_date",
        "follow_up_completed",
        "follow_up_alert",
        "created_at",
        "is_read",
    )

    list_display_links = ("enquiry_id", "name")

    list_filter = (
        "status",
        "priority",
        "lead_source",
        "service",
        "follow_up_completed",
        "follow_up_date",
        "is_read",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "message",
    )

    list_editable = (
        "status",
        "is_read",
        "follow_up_date",
        "follow_up_completed",
    )

    readonly_fields = (
        "enquiry_id",
        "created_at",
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"

    list_per_page = 25

    fieldsets = (
        ("Enquiry Reference", {
            "fields": ("enquiry_id", "created_at")
        }),
        ("Client Information", {
            "fields": ("name", "email", "phone")
        }),
        ("Project Information", {
            "fields": ("service", "message")
        }),
        ("Follow-up Management", {
            "fields": (
                "follow_up_date",
                "follow_up_notes",
                "follow_up_completed",
            )
        }),
        ("Enquiry Management", {
            "fields": ("status", "priority", "lead_source", "is_read")
        }),
    )

    
    @admin.display(description="Follow-up Alert")
    def follow_up_alert(self, obj):

        if not obj.follow_up_date:
            return format_html(
                '<span style="color:#999;">Not Scheduled</span>'
            )

        if obj.follow_up_completed:
            return format_html(
                '<span style="color:#36b88b;font-weight:bold;">Completed</span>'
            )

        today = timezone.localdate()

        if obj.follow_up_date < today:
            return format_html(
                '<span style="background:#fee2e2;color:#b91c1c;'
                'padding:5px 9px;border-radius:6px;font-weight:bold;">'
                'OVERDUE</span>'
            )

        if obj.follow_up_date == today:
            return format_html(
                '<span style="background:#fef3c7;color:#92400e;'
                'padding:5px 9px;border-radius:6px;font-weight:bold;">'
                'DUE TODAY</span>'
            )

        return format_html(
            '<span style="background:#dbeafe;color:#1d4ed8;'
            'padding:5px 9px;border-radius:6px;font-weight:bold;">'
            'UPCOMING</span>'
        )

    
    def changelist_view(self, request, extra_context=None):

        enquiries = ContactMessage.objects.all()

        # Main statistics
        total = enquiries.count()

        new_leads = enquiries.filter(status="New").count()

        contacted = enquiries.filter(status="Contacted").count()

        in_discussion = enquiries.filter(
            status="In Discussion"
        ).count()

        converted = enquiries.filter(status="Converted").count()

        rejected = enquiries.filter(status="Rejected").count()

        conversion_rate = (
            round((converted / total) * 100, 1)
            if total > 0 else 0
        )

        # Monthly enquiry statistics - Last 6 months
        monthly_data = (
            enquiries
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )

        monthly_counts = {
            item["month"].strftime("%Y-%m"): item["total"]
            for item in monthly_data
        }

        today = timezone.localdate()

        monthly_stats = []

        for offset in range(5, -1, -1):

            month_index = today.year * 12 + today.month - 1 - offset

            year = month_index // 12
            month = month_index % 12 + 1

            month_date = date(year, month, 1)

            month_key = month_date.strftime("%Y-%m")

            monthly_stats.append({
                "month": month_date,
                "total": monthly_counts.get(month_key, 0),
            })

        # Monthly progress bar percentages
        max_monthly = max(
            (item["total"] for item in monthly_stats),
            default=0
        )

        for item in monthly_stats:
            item["percentage"] = round(
                (item["total"] / max_monthly) * 100,
                1
            ) if max_monthly else 0

        # Most requested services
        service_stats = list(
            enquiries
            .exclude(service="")
            .values("service")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        # Service progress bar percentages
        max_service = max(
            (item["total"] for item in service_stats),
            default=0
        )

        for item in service_stats:
            item["percentage"] = round(
                (item["total"] / max_service) * 100,
                1
            ) if max_service else 0

        # Follow-up management statistics
        overdue_followups = enquiries.filter(
            follow_up_date__lt=today,
            follow_up_completed=False
        ).exclude(follow_up_date__isnull=True).count()

        today_followups = enquiries.filter(
            follow_up_date=today,
            follow_up_completed=False
        ).count()

        upcoming_followups = enquiries.filter(
            follow_up_date__gt=today,
            follow_up_completed=False
        ).count()

        completed_followups = enquiries.filter(
            follow_up_completed=True
        ).count()

        # Client Follow-up Lists

        overdue_followup_list = enquiries.filter(
            follow_up_date__lt=today,
            follow_up_completed=False
        ).order_by("follow_up_date")[:10]

        today_followup_list = enquiries.filter(
            follow_up_date=today,
            follow_up_completed=False
        ).order_by("follow_up_date")[:10]

        upcoming_followup_list = enquiries.filter(
            follow_up_date__gt=today,
            follow_up_completed=False
        ).order_by("follow_up_date")[:10]
        
        # Dashboard context
        extra_context = extra_context or {}

        extra_context.update({
            "total_enquiries": total,
            "new_leads": new_leads,
            "contacted": contacted,
            "in_discussion": in_discussion,
            "converted_clients": converted,
            "rejected": rejected,
            "conversion_rate": conversion_rate,
            "monthly_stats": monthly_stats,
            "service_stats": service_stats,
            "overdue_followups": overdue_followups,
            "today_followups": today_followups,
            "upcoming_followups": upcoming_followups,
            "completed_followups": completed_followups,
            "overdue_followup_list": overdue_followup_list,
            "today_followup_list": today_followup_list,
            "upcoming_followup_list": upcoming_followup_list,
        })

        return super().changelist_view(
            request,
            extra_context=extra_context
        )

@admin.register(FollowUpActivity)
class FollowUpActivityAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "enquiry",
        "contact_method",
        "contact_date",
        "next_follow_up_date",
    )

    list_display_links = ("id", "enquiry")

    list_filter = (
        "contact_method",
        "contact_date",
        "next_follow_up_date",
    )

    search_fields = (
        "enquiry__name",
        "enquiry__phone",
        "enquiry__email",
        "discussion_details",
        "client_response",
    )

    readonly_fields = (
        "contact_date",
        "created_at",
    )

    date_hierarchy = "contact_date"

    list_select_related = ("enquiry",)

    ordering = ("-contact_date",)

    fieldsets = (
        ("Client Information", {
            "fields": ("enquiry",)
        }),
        ("Contact Details", {
            "fields": (
                "contact_date",
                "contact_method",
                "discussion_details",
                "client_response",
            )
        }),
        ("Next Follow-up", {
            "fields": ("next_follow_up_date",)
        }),
        ("System Information", {
            "fields": ("created_at",)
        }),
    )
