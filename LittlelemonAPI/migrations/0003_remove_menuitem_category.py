# Generated by Django 5.0 on 2024-01-03 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LittlelemonAPI', '0002_category_menuitem_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='category',
        ),
    ]
