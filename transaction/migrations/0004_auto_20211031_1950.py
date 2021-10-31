# Generated by Django 3.0.9 on 2021-10-31 19:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0003_auto_20211031_1737'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='tranaction_id',
            new_name='transaction_id',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='success',
        ),
        migrations.AddField(
            model_name='transaction',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
