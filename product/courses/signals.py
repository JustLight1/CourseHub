from django.db.models import Count
from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver

from users.models import Subscription
from courses.models import Group


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """

    if created and instance.is_active:
        user = instance.user
        course = instance.course
        groups = Group.objects.filter(course=course)
        if not groups.exists():
            return
        sorted_groups = groups.annotate(
            student_count=Count('students')).order_by('student_count')
        suitable_group = None
        for group in sorted_groups:
            if group.students.count() < group.max_students:
                suitable_group = group
                break

        if suitable_group is None and sorted_groups:
            suitable_group = sorted_groups[0]

        if suitable_group:
            with transaction.atomic():
                suitable_group.students.add(user)
                suitable_group.save()
