from django import template
from django.template.defaultfilters import stringfilter
from badwords import badwords

register = template.Library()


@register.filter(name="censor")
@stringfilter
def censor(value):
    value_split = value.split(" ")
    value_cens = ""
    for i in value_split:
        if i.lower() in badwords:
            value_cens += "ups! "
        else:
            value_cens += i + " "
    return value_cens
