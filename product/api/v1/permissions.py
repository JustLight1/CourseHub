from django.db import transaction
from rest_framework import status
from rest_framework.permissions import BasePermission, SAFE_METHODS

from courses.models import Course
from users.models import CustomUser, Subscription


def make_payment(request, course):
    try:
        user = request.user
        with transaction.atomic():
            if Subscription.objects.filter(
                user=user,
                course=course,
                is_active=True
            ).exists():
                return (
                    {"detail": "Вы уже купили этот курс."},
                    status.HTTP_400_BAD_REQUEST
                )

            user_balance = user.balance
            if user_balance.amount < course.price:
                return (
                    {"detail": "Недостаточно средств для покупки курса."},
                    status.HTTP_400_BAD_REQUEST
                )

            user_balance.amount -= course.price
            user_balance.save()

            subscription = Subscription.objects.create(
                user=user,
                course=course,
                is_active=True
            )

            data = {
                "course": course.title,
                "price": course.price,
                "subscription_id": subscription.id,
                "message": "Курс успешно приобретен, доступ к курсу открыт."
            }

        return data, status.HTTP_201_CREATED

    except Exception as e:
        return (
            {"detail": f"Ошибка при обработке платежа: {str(e)}"},
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.groups.filter(
            name='students'
        ).exists()

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if isinstance(obj, Subscription):
            return obj.user == request.user
        if isinstance(obj, Course):
            return obj.subscriptions.filter(
                user=request.user,
                is_active=True
            ).exists()
        if isinstance(obj, CustomUser):
            return obj == request.user
        return False


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
