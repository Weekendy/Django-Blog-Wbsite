# Generated by Django 4.2.3 on 2023-08-24 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0008_alter_blogwatchlog_user_property'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userproperty',
            name='profile',
        ),
        migrations.AddField(
            model_name='usermessage',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='to_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accepted_message', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sended_message', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserProfileMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activate', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/user_porfile/')),
                ('owner', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_media', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
