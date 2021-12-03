from io import BytesIO
from django.db import models
from django.db.models.signals import post_save
from invoices.utils import render_to_pdf
from django.core.files import File

class Invoice(models.Model):
    order_invoice=models.OneToOneField('orders.Order',on_delete=models.CASCADE)
    invoice_pdf=models.FileField(upload_to="invoices")

    def update_pdf(self,pdf=None,filename="orderinvoice"):
        self.invoice_pdf.save(filename,File(BytesIO(pdf.content)))

    def __str__(self):
        return "Invoice for Order "+str(self.order_invoice.id)