from django import template
from datetime import date
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})

@register.filter(name='addcontrols')
def addcontrols(field, argstr):
    parts = argstr.split(",")
    css = parts[0] if len(parts) >= 1 else ""
    placeholder = parts[1] if len(parts) >= 2 else ""
    return field.as_widget(attrs={"class": css, "placeholder": placeholder})

@register.filter(name='age')
def age(field):
    today = date.today()
    return today.year - field.year - ((today.month, today.day) < (field.month, field.day))

@register.filter(name='rating')
def rating(field):
    stars = int(float(field) / 2)
    return stars

@register.filter
def get_range(value):
    return range(value)