# Generated by Django 3.2.9 on 2021-12-02 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_pdf',
            field=models.FileField(upload_to='invoices/'),
        ),
    ]