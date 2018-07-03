from django.contrib import admin
from .models import Author
from .models import Book
from .models import Genre
from .models import BookInstance
from .models import Language
from .models import Transaction
# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)
admin.site.register(Language)
admin.site.register(Transaction)

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'id',)
    list_filter = ('status',)

    fieldsets = (
        (None, {
            'fields': ('book', 'id',)
        }),
        ('Availability', {
            'fields': ('status', )
        }),
    )