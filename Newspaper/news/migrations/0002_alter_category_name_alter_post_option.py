# Generated by Django 4.1.4 on 2023-01-14 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=144, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='option',
            field=models.CharField(choices=[('news', 'Новость'), ('post', 'Публикация')], max_length=4),
        ),
    ]
