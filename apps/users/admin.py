from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, UserProfile, TailorProfile


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )


@admin.register(TailorProfile)
class TailorProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'get_username', 'phone_number', 'location', 'clothing_type', 'approval_status_badge']
    list_filter = ['approval_status', 'clothing_type']
    search_fields = ['full_name', 'user__username', 'phone_number']
    list_per_page = 20
    actions = ['approve_tailors', 'reject_tailors']

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def approval_status_badge(self, obj):
        colors = {'approved': 'green', 'rejected': 'red', 'pending': 'orange'}
        labels = {'approved': '✅ Ameidhinishwa', 'rejected': '❌ Amekataliwa', 'pending': '⏳ Anasubiri'}
        color = colors.get(obj.approval_status, 'gray')
        label = labels.get(obj.approval_status, obj.approval_status)
        return format_html('<span style="color:{}; font-weight:bold;">{}</span>', color, label)
    approval_status_badge.short_description = 'Hali ya Tailor'

    @admin.action(description='✅ Idhinisha Tailor waliochaguliwa')
    def approve_tailors(self, request, queryset):
        updated = queryset.update(approval_status='approved')
        self.message_user(request, f'{updated} tailor wameidhinishwa.')

    @admin.action(description='❌ Kataa Tailor waliochaguliwa')
    def reject_tailors(self, request, queryset):
        updated = queryset.update(approval_status='rejected')
        self.message_user(request, f'{updated} tailor wamekataliwa.')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
