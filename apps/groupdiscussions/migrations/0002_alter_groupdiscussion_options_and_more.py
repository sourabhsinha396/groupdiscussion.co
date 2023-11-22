# Generated by Django 4.2.7 on 2023-11-18 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groupdiscussions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupdiscussion',
            options={'ordering': ('start_datetime',), 'verbose_name': 'Group Discussion', 'verbose_name_plural': 'Group Discussions'},
        ),
        migrations.RenameField(
            model_name='groupdiscussion',
            old_name='start_date',
            new_name='start_datetime',
        ),
        migrations.RemoveField(
            model_name='groupdiscussion',
            name='start_time',
        ),
    ]
