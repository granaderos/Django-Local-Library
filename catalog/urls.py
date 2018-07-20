from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('transactions/', views.TransactionsListView.as_view(), name='transactions'),
    #path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('book/<int:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
    # path('transaction/create/', views.TransactionCreate.as_view(), name='transaction-create'),
    path('transaction/create/', views.create_new_transaction, name='transaction-create'),
    path('book/<int:pk>/return/', views.return_book, name='return-book'),
    path('transaction/history/', views.TransactionHistoryListView.as_view(), name='transaction-history'),
    path('book/<int:pk>/add-instance/', views.create_book_instance, name='add-book-instance'),
    path('user/new', views.create_new_user, name='user-create'),
    path('users', views.UserListView.as_view(), name='users'),
    path('book/<uuid:pk>/update-status/', views.update_book_status, name='update-book-status'),
    path('books/search_book', views.search_book, name='search_book'),
    path('authors/search_author', views.search_author, name='search_author'),
    
]