# Generated by Django 4.0.4 on 2022-05-04 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_book_user_usertobook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('issued', 'ISSUED'), ('returned', 'RETURNED')], default='issued', max_length=30),
        ),
    ]
