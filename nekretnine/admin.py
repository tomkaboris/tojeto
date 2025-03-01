from django.contrib import admin
from .models import CustomUser, SuperUser, CustomUserType

# Customize the admin site
admin.site.site_header = "Moderator Nekretnina"  # Title on the login page
admin.site.site_title = "Moderator Portal"  # Title on the browser tab
admin.site.index_title = "Welcome to the Moderator Dashboard"  # Title on the index page


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'phone_number', 'consent')
    list_filter = ('user_type', 'consent')
    search_fields = ('email', 'username')
    ordering = ('email',)

    def get_queryset(self, request):
        # Exclude superusers from admin view
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False)
    
@admin.register(SuperUser)
class SuperUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_staff',)

@admin.register(CustomUserType)
class CustomUserTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)