from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Post


class BookSearchForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50, required=False)

    def validate_ISBN(value):
        print(not(f'{value}'.isnumeric()))
        if (value != None and (len(value) != 10 and len(value) != 13)):
            print(value)
            raise ValidationError(f'number of digits in {value} is neither 10 nor 13',
                                  params={'value': value},
                                  )
        elif (not(f'{value}'.isnumeric())):
            raise ValidationError(f'{value} has non-numeric elements',
                                  params={'value': value},
                                  )

    ISBN = forms.CharField(label="ISBN", max_length=13,
                           validators=[validate_ISBN], required=False)

    author = forms.CharField(label="Author", max_length=50, required=False)
    edition = forms.IntegerField(
        label="Edition", min_value=1, max_value=15, required=False)
    price = forms.IntegerField(
        label="Maximum price", min_value=1, max_value=15, required=False)
    posted_since = forms.DateField(
        label='posted since, ', initial="2020-04-08", widget=forms.SelectDateWidget, required=False)
