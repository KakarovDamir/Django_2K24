# Generated by Django 5.1.3 on 2024-11-18 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField(verbose_name='Date of Birth')),
                ('registration_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
