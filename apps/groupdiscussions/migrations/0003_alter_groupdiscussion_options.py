# Generated by Django 4.2.7 on 2023-12-11 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groupdiscussions', '0002_alter_groupdiscussion_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupdiscussion',
            options={'ordering': ('start_datetime',), 'verbose_name': 'Interview', 'verbose_name_plural': 'Interviews'},
        ),
    ]