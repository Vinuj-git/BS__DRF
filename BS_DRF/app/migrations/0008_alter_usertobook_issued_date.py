# Generated by Django 4.0.4 on 2022-05-04 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_rename_price_usertobook_user_price_book_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertobook',
            name='issued_date',
            field=models.DateTimeField(),
        ),
    ]
