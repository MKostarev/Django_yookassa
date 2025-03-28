from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
#from api.models import Payment_model
from django.db import transaction
from django.views.generic import ListView
from yookassa import Configuration, Payment

import var_dump as var_dump
import pprint
#import config
import os
import django

from api import config

#from .models import Payment_model

#Настройка Django-окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_yookassa.settings')
django.setup()

# Конфигурация
Configuration.account_id = config.id_shop
Configuration.secret_key = config.api_key

def fetch_payments(limit=100, created_at_gte="2025-01-8T00:00:00.000Z", created_at_lt="2025-02-10T00:00:00.000Z"):
    print("Собираем платежи")
    # Инициализация параметров запроса
    data = {
        "limit": limit,
        "paid": True,  # Добавляем фильтр для оплаченных платежей
        "status": "succeeded",  # Добавляем фильтр по статусу (значение "paid" - оплачен)
        "created_at.gte": created_at_gte,  # Созданы начиная с 2020-08-08
        "created_at.lt": created_at_lt     # И до 2025-03-20
    }
    #Инициализация переменных
    cursor = None
    all_payments = []  # Список для хранения всех платежей

    while True:
        params = data
        if cursor:
            params['cursor'] = cursor

        try:
            res = Payment.list(params)
            print("Количество платежей: " + str(len(res.items)))    # Количество платежей в выборке
            print("Cursor: " + str(res.next_cursor))  # Указатель на следующую страницу

            all_payments.extend(res.items) # Добавляем платежи в общий список

            #var_dump.var_dump(res) # Вывод содержимого объекта

            if not res.next_cursor:
                break
            else:
                cursor = res.next_cursor
        except Exception as e:
            print("Error: " + str(e))
            break
    #print(all_payments[0])
    return all_payments  # Возвращаем все полученные платежи


def filter_payments(payments):
    print("Фильтруем платежи")
    #if not filtered_payments:
        #print("Отфильтрованные платежи пустые!")
    """
    Фильтрует данные о платежах, оставляя только нужные поля.
    :param payments: Список объектов PaymentResponse.
    :return: Отфильтрованный список платежей.
    """
    filtered_data = []
    for payment in payments:
        filtered_data.append({
            "payment_id": payment._PaymentResponse__id,  # Уникальный идентификатор платежа
            "status": payment._PaymentResponse__status,  # Статус платежа (успешно/отклонено/ожидает)
            "amount_value": float(payment._PaymentResponse__amount._Amount__value),  # Сумма платежа в числовом формате
            "amount_currency": payment._PaymentResponse__amount._Amount__currency,  # Валюта платежа (USD, RUB и т.д.)
            "seminar": payment._PaymentResponse__description,  # Описание платежа
            "date": payment._PaymentResponse__created_at, #дата создания платежа
            "cps_phone": payment._PaymentResponse__metadata.get('cps_phone'),  # Телефон клиента
            "cust_name": payment._PaymentResponse__metadata.get('custName'),  # Имя клиента
            "cps_email": payment._PaymentResponse__metadata.get('cps_email'),  # Email клиента
            "cms_name": payment._PaymentResponse__metadata.get('cms_name'),  # Название используемой CMS
            "details_party": payment._PaymentResponse__payment_method,  # метод оплаты
        })
    print(filtered_data)
    return filtered_data


def save_payments_to_db(filtered_payments):
    #print(f"Заходим в функцию сохранения платежей") # Добавленный лог
    """
    Сохраняет отфильтрованные данные о платежах в базу данных.
    :param filtered_payments: Список словарей с данными о платежах.
    """
    with transaction.atomic():
        try:
            for payment_data in filtered_payments:
                print(f"Сохраняем платежи")  # Добавленный лог
                # Создаём или обновляем запись в базе данных
                from api.models import Payment_model
                payment, created = Payment_model.objects.update_or_create(
                    payment_id=payment_data.get("payment_id"),
                    defaults={
                        "status": payment_data.get("status"),
                        "amount_value": payment_data.get("amount_value"),
                        "amount_currency": payment_data.get("amount_currency"),
                        "seminar": payment_data.get("description"),
                        "date": payment_data.get("date"),
                        "cps_phone": payment_data.get("cps_phone"),
                        "cust_name": payment_data.get("cust_name"),
                        "cps_email": payment_data.get("cps_email"),
                        "cms_name": payment_data.get("cms_name"),
                        "details_party": payment_data.get("details_party"),
                    }
                )
                if created:
                    print(f"Создан новый платеж: {payment.payment_id}")
                else:
                    print(f"Обновлено: {payment.payment_id}")
        except Exception as e:
            print(f"Ошибка при сохранении платежа: {str(e)}")




from django.db import transaction
from api.models import Student, Seminar, Seminar_studet, SeminarRegistration, Payment_model


def save_student(filtered_payments):
    print('Сохраняем студентов')
    students = []
    """
    Сохраняет или обновляет данные студента.
    :param filtered_payments: Список словарей с данными о платежах.
    """
    for payment_data in filtered_payments:  # Перебираем каждый элемент списка
        student, created = Student.objects.update_or_create(
            student_email=payment_data.get("cps_email"),  # Уникальное поле
            defaults={
                "student_name": payment_data.get("cust_name"),
                "student_phone": payment_data.get("cps_phone"),
            }
        )
        if created:
            print(f"Создан новый студент: {student.student_email}")
        else:
            print(f"Обновлен студент: {student.student_email}")
        students.append(student)  # Добавляем студента в список
    print(students)
    return students


def save_seminar(filtered_payments):
    print('Сохраняем семинары')
    seminars = []
    """
    Сохраняет или обновляет данные семинара.
    :param filtered_payments: Список словарей с данными о платежах.
    """
    for payment_data in filtered_payments:  # Перебираем каждый элемент списка
        seminar, created = Seminar.objects.get_or_create(
            seminar_name=payment_data.get("seminar"),  # Используем seminar_name
            defaults={
                "description": payment_data.get("description", ""),  # Описание семинара (если есть)
            }
        )
        if created:
            print(f"Создан новый семинар: {seminar.seminar_name}")
        else:
            print(f"Обновлен семинар: {seminar.seminar_name}")
        seminars.append(seminar)  # Добавляем семинар в список
    print(seminars)
    return seminars


#def save_seminar_students(students, seminars):
#    try:
#        # Получаем все существующие связи для оптимизации
#        existing_links = Seminar_studet.objects.filter(
#            student__in=students,
#            seminar__in=seminars
#        ).values_list('student_id', 'seminar_id')
#
#        # Создаем словарь существующих связей для быстрой проверки
#        existing_links_dict = {(s, e) for s, e in existing_links}
#
#        for student in students:
#            # Предполагаем, что у каждого студента есть поле с семинарами
#            # Например, список названий семинаров, на которые он записан
#            student_seminars = student.seminars  # или как это у вас реализовано
#
#            for seminar_name in student_seminars:
#                # Находим конкретный семинар для студента
#                seminar = seminars.filter(seminar_name=seminar_name).first()
#
#                if seminar:
#                    # Проверяем, существует ли уже такая связь
#                    if (student.id, seminar.id) not in existing_links_dict:
#                        # Создаем связь только если её нет
#                        seminar_student, created = Seminar_studet.objects.get_or_create(
#                            seminar=seminar,
#                            student=student
#                        )
#                        if created:
#                            print(f"Создана связь: {student.student_name} -> {seminar.seminar_name}")
#                        else:
#                            print(f"Связь уже существует: {student.student_name} -> {seminar.seminar_name}")
#                    else:
#                        print(f"Связь уже существует: {student.student_name} -> {seminar.seminar_name}")
#    except Exception as e:
#        print(f"Ошибка при создании связи: {str(e)}")
#
#
## Теперь вызываем функцию правильно



def group_students_by_seminar(payments):
    print('Группирует студентов по семинарам, для каждого семинара указан список студентов.')
    """
    Группирует студентов по семинарам.
    :param payments: Список объектов PaymentResponse.
    :return: Список словарей, где для каждого семинара указан список студентов.
    """
    seminars = {}  # Словарь для хранения данных о семинарах и студентах

    for payment in payments:
        seminar_name = payment.description  # Название семинара
        student_data = {
            "student_name": payment.metadata.get("custName"),  # ФИО студента
            "student_email": payment.metadata.get("cps_email"),  # Почта студента
            "student_phone": payment.metadata.get("cps_phone"),  # Телефон студента
        }

        # Если семинар уже есть в словаре, добавляем студента
        if seminar_name in seminars:
            seminars[seminar_name].append(student_data)
        else:
            # Если семинара нет, создаем новую запись
            seminars[seminar_name] = [student_data]

    # Преобразуем словарь в список
    result = [{"seminar": seminar, "students": students} for seminar, students in seminars.items()]
    print(result)
    return result


#def save_seminars_data(data):
#    try:
#        # Создаем список для хранения созданных студентов
#        students = []
#        # Создаем список для хранения созданных семинаров
#        seminars = []
#
#        # Проходим по каждому семинару из входных данных
#        for seminar_item in data:
#            # Получаем название семинара
#            seminar_name = seminar_item.get('seminar')
#
#            # Проверяем, существует ли семинар
#            seminar, created = Seminar.objects.get_or_create(
#                seminar_name=seminar_name,
#                defaults={
#                    "description": seminar_item.get("description", "")
#                }
#            )
#
#            if created:
#                print(f"Создан новый семинар: {seminar.seminar_name}")
#            else:
#                print(f"Обновлен семинар: {seminar.seminar_name}")
#
#            seminars.append(seminar)
#
#            # Проходим по каждому студенту в семинаре
#            for student_data in seminar_item.get('students', []):
#                # Получаем данные студента
#                student_email = student_data.get('student_email')
#
#                # Проверяем, существует ли студент
#                student, created = Student.objects.update_or_create(
#                    student_email=student_email,
#                    defaults={
#                        "student_name": student_data.get('student_name'),
#                        "student_phone": student_data.get('student_phone')
#                    }
#                )
#
#                if created:
#                    print(f"Создан новый студент: {student.student_email}")
#                else:
#                    print(f"Обновлен студент: {student.student_email}")
#
#                students.append(student)
#
#                # Проверяем, существует ли уже такая связь
#                if not Seminar_studet.objects.filter(seminar=seminar, student=student).exists():
#                    # Создаем связь между семинаром и студентом
#                    seminar_student, created = Seminar_studet.objects.get_or_create(
#                        seminar=seminar,
#                        student=student
#                    )
#
#                    if created:
#                        print(f"Создана связь: {student.student_name} -> {seminar.seminar_name}")
#                    else:
#                        print(f"Связь уже существует: {student.student_name} -> {seminar.seminar_name}")
#
#        return {
#            'students': students,
#            'seminars': seminars
#        }
#
#    except Exception as e:
#        print(f"Произошла ошибка: {str(e)}")
#        return None


#
#
def save_seminar_registrations(seminars_data):
    """
    Сохраняет данные о регистрациях на семинары без использования связей
    :param seminar_data: Список словарей с данными о семинарах и студентах
    """
    created_seminars = []

    for seminar_data in seminars_data:
        # Сохраняем семинар
        seminar, _ = Seminar.objects.get_or_create(
            seminar_name=seminar_data['seminar'],
            defaults={'description': ''}  # Можно добавить описание, если оно есть в данных
        )

        # Подготавливаем данные студентов для сохранения
        students_payments_data = [
            {
                "cps_email": student['student_email'],
                "cust_name": student['student_name'],
                "cps_phone": student['student_phone'],
                "seminar": seminar_data['seminar']
            }
            for student in seminar_data['students']
        ]

        # Сохраняем студентов
        students = save_student(students_payments_data)

        # Создаем связи между семинаром и студентами
        for student in students:
            Seminar_studet.objects.get_or_create(
                seminar=seminar,
                student=student
            )

        created_seminars.append({
            'seminar': seminar,
            'students': students
        })

    return created_seminars


class IndexrealtyView(ListView):
    template_name = 'profile.html'
    model = Seminar
    context_object_name = 'seminar_student_data'



payments_data = fetch_payments() # Получаем данные от API
filtered_payments = filter_payments(payments_data) #Фильтруем данные в базе
save_payments_to_db(filtered_payments)# Сохраняем данные в базу
student = save_student(filtered_payments)# Сохраняем данные студентов в базу
#seminar = save_seminar(filtered_payments)# Сохраняем данные семирана в базу
#save_seminar_students(student, seminar)

#students = save_students(filtered_payments)
#seminars = save_seminars(filtered_payments)
#save_seminar_students(students, seminars)

data = group_students_by_seminar(payments_data)
#save_seminars_data(data)
save_seminar_registrations(data)

# Выводим отфильтрованные данные
#pprint.pprint(filtered_payments)
