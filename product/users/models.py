from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

from courses.models import Course


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)
            Balance.objects.create(user=self)
        else:
            super().save(*args, **kwargs)


class Balance(models.Model):
    """Модель баланса пользователя."""

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='balance',
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1000,
        verbose_name='Баланс',
        validators=[MinValueValidator(0)],
    )

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.amount}'


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь',
        db_index=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Курс',
        db_index=True,
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Активная подписка',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.course}'
