# Generated by Django 4.2.18 on 2025-03-22 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('amount_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('amount_currency', models.CharField(blank=True, max_length=3, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('payment_method_type', models.CharField(blank=True, max_length=50, null=True)),
                ('payment_method_id', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_method_title', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_method_account_number', models.CharField(blank=True, max_length=50, null=True)),
                ('cps_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('cust_name', models.CharField(blank=True, max_length=100, null=True)),
                ('cms_name', models.CharField(blank=True, max_length=100, null=True)),
                ('cps_email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('amount_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('amount_currency', models.CharField(blank=True, max_length=3, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('date', models.CharField(blank=True, max_length=100, null=True)),
                ('cps_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('cust_name', models.CharField(blank=True, max_length=100, null=True)),
                ('cps_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('cms_name', models.CharField(blank=True, max_length=100, null=True)),
                ('details_party', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seminar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seminar_name', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(blank=True, max_length=100, null=True)),
                ('cps_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('cps_email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
    ]
