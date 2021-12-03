import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .utils import render_to_pdf
from .models import Invoice

def generatepdf_view(request,id):
    invoice=Invoice.objects.get(order_invoice=id)
    billing_profile=invoice.order_invoice.billing_profile
    full_name=invoice.order_invoice.billing_address.full_name
    email=invoice.order_invoice.billing_profile.email
    contact_no = invoice.order_invoice.billing_address.contact_no
    shipping_address=invoice.order_invoice.shipping_address
    billing_address=invoice.order_invoice.billing_address
    status=invoice.order_invoice.status
    shipping_total=invoice.order_invoice.shipping_total
    finaltotal=invoice.order_invoice.finaltotal
    cart=invoice.order_invoice.cart
    item=invoice.order_invoice.cart.items.all()
    active=invoice.order_invoice.active
    updated=invoice.order_invoice.updated
    timestamp=invoice.order_invoice.timestamp
    gst_rate=round(0.05* float(finaltotal),3)
    with_gst_total=gst_rate+float(finaltotal)
    data = {
        'today': datetime.date.today(),
        'billing_profile':billing_profile,
        'full_name':full_name,
        'email':email,
        'contact_no':contact_no,
        'shipping_address':shipping_address,
        'billing_address':billing_address,
        'status':status,
        'shipping_total':shipping_total,
        'finaltotal':finaltotal,
        'cart':cart,
        'item':item,
        'active':active,
        'updated':updated,
        'timestamp':timestamp,
        'customer_name': 'Cooper Mann',
        'order_id': id,
        'gst_rate':gst_rate,
        'with_gst_total':with_gst_total,
    }
    pdf = render_to_pdf('invoices/invoice.html', data)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_for_order_%s.pdf" % (invoice.order_invoice.id)
        content = "inline; filename='%s'" % (filename)
        invoice.update_pdf(pdf,filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not Found")
