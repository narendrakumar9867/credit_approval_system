# Generated by Django 5.2.1 on 2025-06-11 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_rename_customer_id_loan_customer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="loan_id",
            field=models.CharField(max_length=5000),
        ),
    ]
