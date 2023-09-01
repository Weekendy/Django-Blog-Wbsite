# Generated by Django 4.2.3 on 2023-08-12 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0010_remove_blogpost_image_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='image_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='blogpostmedia',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/blogpost_photo/'),
        ),
    ]