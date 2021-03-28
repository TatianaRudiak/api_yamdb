# Generated by Django 3.1.7 on 2021-03-27 11:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yamdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-id'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['role'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['-id'], 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['-id'], 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(2021)], verbose_name='Дата выхода'),
        ),
    ]