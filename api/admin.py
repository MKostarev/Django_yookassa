from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Payment_model, Seminar, Student, Seminar_studet, SeminarRegistration

#admin.site.register(Payment_model)

class SeminarStudentInline(admin.TabularInline):  # Или admin.StackedInline для другого стиля
    model = Seminar_studet
    extra = 0  # Не показывать пустые формы для добавления
    readonly_fields = ('student',)  # Сделать поле студента только для чтения

class Payment_modelAdmin(admin.ModelAdmin):
    list_display = ['cust_name', 'date', 'seminar', 'amount_value', 'amount_currency']  # Список полей, которые вы хотите отобразить

admin.site.register(Payment_model, Payment_modelAdmin)

#@admin.register(Seminar)
class SeminarAdmin(admin.ModelAdmin):
    list_display = ['seminar_name']  # Список полей, которые вы хотите отобразить
    search_fields = ('seminar_name',)  # Поиск по названию семинара
    inlines = [SeminarStudentInline]  # Добавляем inline-админку

admin.site.register(Seminar, SeminarAdmin)

#@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_phone', 'student_email')  # Поля для отображения
    search_fields = ('student_name', 'student_email')  # Поиск по имени и email

admin.site.register(Student, StudentAdmin)

#@admin.register(Seminar_studet)
class Seminar_studetAdmin(admin.ModelAdmin):
    list_display = ('seminar', 'student')  # Поля для отображения
    list_filter = ('seminar',)  # Фильтр по семинарам
    search_fields = ('student__student_name', 'seminar__seminar_name')  # Поиск по имени студент

admin.site.register(Seminar_studet, Seminar_studetAdmin)

class SeminarRegistrationAdmin(admin.ModelAdmin):
    class SeminarRegistrationAdmin(admin.ModelAdmin):
        list_display = ('seminar_link', 'student_name', 'student_email', 'student_phone')
        list_filter = ('seminar_name',)
        search_fields = ('seminar_name', 'student_name', 'student_email')

        def seminar_link(self, obj):
            url = reverse('admin:app_seminaregistration_changelist') + f'?seminar_name={obj.seminar_name}'
            return format_html('<a href="{}">{}</a>', url, obj.seminar_name)

        seminar_link.short_description = "Семинар"
        seminar_link.admin_order_field = 'seminar_name'


admin.site.register(SeminarRegistration, SeminarRegistrationAdmin)


