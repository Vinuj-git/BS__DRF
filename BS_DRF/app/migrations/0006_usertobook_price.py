# Generated by Django 4.0.4 on 2022-05-04 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_usertobook_issued_date_usertobook_returned_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertobook',
            name='price',
            field=models.DecimalField(decimal_places=2, default=88.0, max_digits=6),
            preserve_default=False,
        ),
    ]
