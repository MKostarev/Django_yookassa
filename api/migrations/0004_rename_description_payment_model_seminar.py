# Generated by Django 4.2.18 on 2025-03-23 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_cps_email_student_student_email_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment_model',
            old_name='description',
            new_name='seminar',
        ),
    ]
