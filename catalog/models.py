from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from datetime import datetime

import uuid

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book.')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 character ISBN number.')
    imprint = models.CharField(max_length=200, null=True, help_text="Enter imprint information of the book.")
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book.')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    copies = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class Language(models.Model):

    LANGUAGES = [
        ('English', 'English'), 
        ('Filipino', 'Filipino'),
        ('German', 'German'),
    ]

    name = models.CharField(max_length=100, choices=LANGUAGES, blank=True)

    def __str__(self):
        return self.name



class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    # class Meta:
    #     ordering = ['due_back']
    #     permissions = (('can_mark_returned', 'Set book as returned'),)

    def __str__(self):
        return '{0} ({1})'.format(self.book.title, self.id)

    @property
    def is_overdue(self):
        if self.due_back and datetime.today() > self.due_back:
            return True
        return False


class Transaction(models.Model):
    book_instance = models.ForeignKey(BookInstance, on_delete=models.SET_NULL, null=True)
    date_borrowed = models.DateField(default=datetime.now)
    due_back = models.DateField(null=True, blank=True)
    date_returned = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    remark = models.TextField(max_length=1000, null=True, help_text="Condition of the book when returned.")


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Dies', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)
