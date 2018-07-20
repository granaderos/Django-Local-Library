from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import BookInstance
from .models import Book

import datetime


STATUS_VALUES = (
        ('a', 'Available'),
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('r', 'Reserved'),
    )

class CustomAuthenticationForm(AuthenticationForm, forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', "width": "276"}))
    #help_text="Enter a date between now and 4 weeks (default 3)."
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
        book_choices.append((item['id'], id_title_dictionary[item['book']] + ' (' + str(item['id']) + ')'))

    users = User.objects.all().values_list('id', 'username')

    book = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=book_choices)
    date_borrowed = forms.DateField(widget=forms.TextInput(attrs={'value': datetime.date.today(), 'class': 'form-control'}))
    due_date = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control'}))
    borrower = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=users)
    

class ReturnBookForm(forms.Form):
    remarks = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Enter a remark (e.i. condition of the book, etc.)"}))
    date_returned = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control'}))


class CreateBookInstanceForm(forms.Form):
    
    status = forms.ChoiceField(choices=STATUS_VALUES, widget=forms.Select(attrs={'class': 'form-control'}))


class CreateUserForm(forms.Form):
    IS_STAFF_VALUES = (('f', 'NO'), ('t', 'YES'))
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    is_staff = forms.ChoiceField(choices=IS_STAFF_VALUES, widget=forms.Select(attrs={'class': 'form-control'}))
    

class UpdateBookStatusForm(forms.Form):
    new_status = forms.ChoiceField(choices=STATUS_VALUES, widget=forms.Select(attrs={'class': 'form-control'}))
