from django.db import models

from users.models import CustomUser


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость',
    )
    is_available = models.BooleanField(
        default=False,
        verbose_name='Курс доступен для покупки',
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс',
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    title = models.CharField(
        max_length=255,
        verbose_name='Название группы',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='groups',
        verbose_name='Курс',
    )
    max_students = models.PositiveIntegerField(
        verbose_name='Максимальное количество студентов',
        default=30,
    )
    students = models.ManyToManyField(
        CustomUser,
        related_name='student_groups',
        verbose_name='Студенты',
        blank=True,
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)

    def __str__(self):
        return self.title
