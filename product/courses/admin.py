from django.contrib import admin
from .models import Course, Lesson, Group


class LessonInline(admin.TabularInline):
    """Встроенная форма для управления уроками в админке курса."""

    model = Lesson
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    """Админка для модели курса."""

    model = Course
    list_display = (
        'id', 'title', 'author', 'start_date', 'price', 'is_available'
    )
    list_filter = ('is_available', 'start_date')
    search_fields = ('title', 'author')
    ordering = ('-start_date',)
    inlines = [LessonInline]


class LessonAdmin(admin.ModelAdmin):
    """Админка для модели урока."""

    model = Lesson
    list_display = ('id', 'title', 'course', 'link')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    ordering = ('course', 'title')


class GroupAdmin(admin.ModelAdmin):
    """Админка для модели группы."""

    model = Group
    list_display = ('id',)
    ordering = ('-id',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Group, GroupAdmin)
