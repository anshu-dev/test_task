# Generated by Django 4.0 on 2021-12-14 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_consumption', '0005_alter_halfhourlydata_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingdatabulkupload',
            name='date_uploaded',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='halfhourlydatabulkupload',
            name='date_uploaded',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='meterdatabulkupload',
            name='date_uploaded',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]