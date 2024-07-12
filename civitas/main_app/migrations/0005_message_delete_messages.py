# Generated by Django 5.0.7 on 2024-07-12 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_groups_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_content', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Messages',
        ),
    ]
