# Django Tempus Dominus

Port of django-tempus-dominus for v6 of Tempus Dominus

## Installation

* [NOT YET AVAILABLE] From PyPI: `pip install django-tempus-dominus-6`

Then add `tempus_dominus_6` to `INSTALLED_APPS` in your Django settings.

## Usage & Django Settings

The following settings are available:

* `TEMPUS_DOMINUS_6_DEFAULT_OPTIONS` (default: `{}`): Default options for each picker instance

Three widgets are provided, no discrepancy is made just now between them:

* `DatePicker`
    * Defaults to `L` if `TEMPUS_DOMINUS_LOCALIZE` is `True`, otherwise `TEMPUS_DOMINUS_DATE_FORMAT`
* `DateTimePicker`
    * Defaults to `L LTS` if `TEMPUS_DOMINUS_LOCALIZE` is `True`, otherwise `TEMPUS_DOMINUS_DATETIME_FORMAT`
* `TimePicker`
    * Defaults to `LTS` if `TEMPUS_DOMINUS_LOCALIZE` is `True`, otherwise `TEMPUS_DOMINUS_TIME_FORMAT`

In your Django form, you can use the widgets like this:

```python
from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

class MyForm(forms.Form):
    date_field = forms.DateField(widget=DatePicker())
    date_field_required_with_min_max_date = forms.DateField(
        required=True,
        widget=DatePicker(
            options={
                  ...
            },
        ),
        initial='2013-01-01',
    )
   ```

## Maintainers

* Steve Bradshaw (https://github.com/st8st8)

