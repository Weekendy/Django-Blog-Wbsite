# Generated by Django 4.2.3 on 2023-07-30 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_blogpostmedia_blogpost_image_num_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpostmedia',
            old_name='active',
            new_name='activete',
        ),
    ]
