# Generated by Django 4.2.3 on 2023-07-28 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_tag_date_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='tag',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='blogposts', to='blogs.tag'),
        ),
    ]
