# Generated by Django 4.2.6 on 2023-10-10 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='chto.png', upload_to='profile_pics'),
        ),
    ]