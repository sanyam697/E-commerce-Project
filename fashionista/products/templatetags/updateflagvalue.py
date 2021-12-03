from django import template

register = template.Library()

def updateflag(product,products):
    flag=False
    for p in products:
        if p.product == product:
            flag=True
            break
    return flag

register.filter(updateflag)