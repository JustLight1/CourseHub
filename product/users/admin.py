from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Balance, Subscription


class CustomUserAdmin(UserAdmin):
    """Админка для кастомной модели пользователя."""

    model = CustomUser
    list_display = ('id', 'email', 'username', 'first_name',
                    'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-id',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name',
                       'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )


class BalanceAdmin(admin.ModelAdmin):
    """Админка для модели баланса пользователя."""

    model = Balance
    list_display = ('id', 'user', 'amount')
    search_fields = ('user__email',)
    ordering = ('-id',)


class SubscriptionAdmin(admin.ModelAdmin):
    """Админка для модели подписки."""

    model = Subscription
    list_display = ('id', 'user', 'course', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('user__email', 'course__title')
    ordering = ('-id',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
