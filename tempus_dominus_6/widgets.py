import json

from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_str
from django.conf import settings
from django.template.loader import render_to_string


def cdn_media():
    """
    Returns the CDN locations for Tempus Dominus, included by default.
    """
    css = {
        "all": (
"https://cdn.jsdelivr.net/npm/@eonasdan/tempus-dominus@6.7.11/dist/css/tempus-dominus.min.css"
        )
    }

    js = (
        (
            "https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"
        ),
        (
            "https://cdn.jsdelivr.net/npm/@eonasdan/tempus-dominus@6.7.11/dist/js/tempus-dominus.min.js",
        ),
    )

    return forms.Media(css=css, js=js)


class TempusDominusMixin:
    """
    The Tempus Dominus Mixin contains shared functionality for the three types of date
    pickers offered.
    """

    def __init__(self, attrs=None, options=None, format=None):
        super().__init__()

        # Set default options 
        self.js_options = {
        }
        # If a dictionary of options is passed, combine it with our pre-set js_options.
        if isinstance(options, dict):
            self.js_options = {**self.js_options, **options}
        # save any additional attributes that the user defined in self
        self.attrs = attrs or {}

    @property
    def media(self):
        if getattr(settings, "TEMPUS_DOMINUS_INCLUDE_ASSETS", True):
            return cdn_media()
        return forms.Media()

    def render(self, name, value, attrs=None, renderer=None):
        context = super().get_context(name, value, attrs)

        # self.attrs = user-defined attributes from __init__
        # attrs = attributes added for rendering.
        # context['attrs'] contains a merge of self.attrs and attrs
        # NB If crispy forms is used, it will already contain
        # 'class': 'datepicker form-control'
        # for DatePicker widget

        all_attrs = context["widget"]["attrs"]
        all_attrs["id"] = all_attrs["id"].replace('-', '_')
        cls = all_attrs.get("class", "")
        if "form-control" not in cls:
            cls = "form-control " + cls

        # Add the attribute that makes datepicker popup close when focus is lost
        cls += " datetimepicker-input"
        all_attrs["class"] = cls

        attr_html = ""
        for attr_key, attr_value in all_attrs.items():
            attr_html += ' {key}="{value}"'.format(key=attr_key, value=attr_value)

        # Bind options into defaults
        options = getattr(settings, "TEMPUS_DOMINUS_6_DEFAULT_OPTIONS", {})
        options.update(self.js_options)

        # picker_id below has to be changed to underscores, as hyphens are not
        # valid in JS function names.
        field_html = render_to_string(
            "tempus_dominus_6/widget.html",
            {
                "type": context["widget"]["type"],
                "picker_id": context["widget"]["attrs"]["id"].replace("-", "_"),
                "name": context["widget"]["name"],
                "value": context["widget"]["value"],
                "attrs": mark_safe(attr_html),
                "js_options": mark_safe(json.dumps(options)),
            },
        )

        return mark_safe(force_str(field_html))



class DatePicker(TempusDominusMixin, forms.widgets.DateInput):
    """
    Widget for Tempus Dominus DatePicker.
    """

    def get_js_format(self):
        if getattr(settings, "TEMPUS_DOMINUS_LOCALIZE", False):
            js_format = "L"
        else:
            js_format = getattr(settings, "TEMPUS_DOMINUS_DATE_FORMAT", "YYYY-MM-DD")
        return js_format


class DateTimePicker(TempusDominusMixin, forms.widgets.DateTimeInput):
    """
    Widget for Tempus Dominus DateTimePicker.
    """

    def get_js_format(self):
        if getattr(settings, "TEMPUS_DOMINUS_LOCALIZE", False):
            js_format = "L LTS"
        else:
            js_format = getattr(settings, "TEMPUS_DOMINUS_DATETIME_FORMAT", "YYYY-MM-DD HH:mm:ss")
        return js_format


class TimePicker(TempusDominusMixin, forms.widgets.TimeInput):
    """
    Widget for Tempus Dominus TimePicker.
    """

    def get_js_format(self):
        if getattr(settings, "TEMPUS_DOMINUS_LOCALIZE", False):
            js_format = "LTS"
        else:
            js_format = getattr(settings, "TEMPUS_DOMINUS_TIME_FORMAT", "HH:mm:ss")
        return js_format
