# Generated by Django 4.2.3 on 2023-08-24 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_userproperty_profile_usermessage_date_added_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproperty',
            name='introduce',
            field=models.TextField(default='这个人很懒，什么也没留下'),
        ),
    ]
