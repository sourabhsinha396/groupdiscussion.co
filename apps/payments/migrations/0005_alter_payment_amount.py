# Generated by Django 4.2.7 on 2023-12-11 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_remove_payment_refered_by_alter_credit_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
