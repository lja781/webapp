from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import *

def linkify(field_name, app_label=None):

    def _linkify(obj):
        nonlocal app_label
        if app_label == None:
            app_label=obj._meta.app_label
        linked_obj = getattr(obj, field_name)
        model_name = linked_obj._meta.model_name
        view_name = f"admin:{app_label}_{model_name}_change"
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_descripton = field_name
    return _linkify

admin.site.register(CV)
admin.site.register(Referee)
admin.site.register(WorkExperience)
admin.site.register(TechSkill)
admin.site.register(Education)
admin.site.register(AddressCV)
admin.site.register(AddressReferee)
