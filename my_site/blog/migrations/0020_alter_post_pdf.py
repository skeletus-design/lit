# Generated by Django 4.2.6 on 2023-12-08 09:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_post_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pdf',
            field=models.FileField(null='true', upload_to='blog/uploads', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]
