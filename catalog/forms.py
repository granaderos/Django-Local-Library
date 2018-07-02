from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from .models import BookInstance
from .models import Book

import datetime


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker', "width": "276"}), help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data


class CreateTransactionForm(forms.Form):
    book_instances = BookInstance.objects.filter(status__exact='a').values('id', 'book')
    books = Book.objects.all().values('id', 'title')

    id_title_dictionary = {}

    book_choices = []

    for item in books:
        id_title_dictionary[item['id']] = item['title']

    for item in book_instances:
        #book_instances[item['id']] = id_title_dictionary[item['book']]
        # book_choices[item['id']] = id_title_dictionary[item['book']]
        book_choices.append((item['id'], id_title_dictionary[item['book']] + ' (' + str(item['id']) + ')'))

    # for key, value in book_instances:
    #     book_inst['id'] = 

    users = User.objects.all().values_list('id', 'username')

    book = forms.ChoiceField(choices=book_choices)
    
    date_borrowed = forms.DateField(widget=forms.TextInput(attrs={'value': datetime.date.today()}))
    due_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))
    borrower = forms.ChoiceField(choices=users)
    

