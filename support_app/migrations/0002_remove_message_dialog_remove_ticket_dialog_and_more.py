# Generated by Django 4.0.6 on 2022-07-04 15:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('support_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='dialog',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='dialog',
        ),
        migrations.AddField(
            model_name='message',
            name='ticket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='support_app.ticket', verbose_name='Тикет'),
        ),
        migrations.AlterField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='TicketDialog',
        ),
    ]
