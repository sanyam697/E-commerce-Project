# Generated by Django 3.2.9 on 2021-12-02 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_alter_invoice_invoice_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_pdf',
            field=models.FileField(upload_to='invoices'),
        ),
    ]