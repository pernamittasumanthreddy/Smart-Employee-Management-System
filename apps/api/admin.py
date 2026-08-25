from django.contrib import admin
from apps.api.models import APIKey, WebhookEndpoint, BiometricDeviceLog

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_active', 'rate_limit_per_minute', 'created_at')

@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_url', 'is_active')

@admin.register(BiometricDeviceLog)
class BiometricDeviceLogAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'biometric_user_id', 'punch_timestamp', 'punch_type', 'is_synced')
