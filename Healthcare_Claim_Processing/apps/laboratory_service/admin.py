@admin.register(LabOrderORMModel)
class LabOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient_id",
        "status_badge",
        "created_at",
    )

    list_filter = ("status",)

    search_fields = (
        "=id",
        "=patient_id",
    )

    readonly_fields = (
        "id",
        "patient_id",
        "encounter_id",
        "ordering_physician_id",
        "status",
        "created_at",
        "updated_at",
    )

    inlines = [
        SpecimenInline,
        DiagnosticReportResultInline,
    ]

    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(description="Status")
    def status_badge(self, obj):
        colors = {
            "REQUESTED": "#0d6efd",
            "SPECIMEN_COLLECTED": "#0dcaf0",
            "PROCESSING": "#ffc107",
            "RESULTED": "#fd7e14",
            "VALIDATED": "#198754",
            "CANCELLED": "#dc3545",
        }

        return format_html(
            '<span style="background:{};color:#fff;padding:3px 8px;'
            'border-radius:4px;font-size:11px;font-weight:bold">{}</span>',
            colors.get(obj.status, "#6c757d"),
            obj.status,
        )