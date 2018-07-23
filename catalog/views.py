from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import edit
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db import connection
from django.db.models import Q
from guardian.shortcuts import assign_perm
from .models import Book
from .models import Author
from .models import BookInstance
from .models import Genre
from .models import Transaction
from .forms import RenewBookForm
from .forms import CreateTransactionForm
from .forms import ReturnBookForm
from .forms import CreateBookInstanceForm
from .forms import CreateUserForm
from .forms import UpdateBookStatusForm

import datetime
import json
# Create your views here.

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_harry_potter_books = Book.objects.filter(title__icontains='Harry Potter').count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1


    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_genres': num_genres,
            'num_harry_potter_books': num_harry_potter_books,
            'num_visits': num_visits
        }
    )

@login_required
@permission_required('catalog.change_trasaction')
def renew_book_librarian(request, pk):
    trans = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            trans.due_back = form.cleaned_data['renewal_date']
            trans.save()

            return HttpResponseRedirect(reverse('transactions'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'trans': trans})

@login_required
@permission_required('catalog.add_transaction')
def create_new_transaction(request):
    # trans = get_object_or_404(Transaction, pk=pk)
    form = CreateTransactionForm(request.POST or None)
    if request.method == 'POST':
        form = CreateTransactionForm(request.POST or None)
        if form.is_valid():
            book_instance = BookInstance.objects.get(id=form.cleaned_data['book'])
            book_instance.status = 'o'
            book_instance.save()

            date_borrowed = form.cleaned_data['date_borrowed']
            due_date = form.cleaned_data['due_date']
            borrower = User.objects.get(id=form.cleaned_data['borrower'])
            trans = Transaction.objects.create(book_instance=book_instance, date_borrowed=date_borrowed, due_back=due_date, borrower=borrower)
            trans.save()
            return HttpResponseRedirect(reverse('transactions'))
    return render(request, 'catalog/create_transaction.html', {'form': form})

@login_required
@permission_required('catalog.change_transaction')
def return_book(request, pk):
    trans = get_object_or_404(Transaction, pk=pk)
    book_instance = get_object_or_404(BookInstance, pk=trans.book_instance.id)
    form = ReturnBookForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            date_returned = form.cleaned_data['date_returned']
            remarks = form.cleaned_data['remarks']

            book_instance.status='a'
            trans.date_returned = date_returned
            trans.remark = remarks

            trans.save()
            book_instance.save()
            return HttpResponseRedirect(reverse('transactions'))

    return render(request, 'catalog/return_book.html', {'form': form, 'trans': trans})

@login_required
@permission_required('catalog.add_bookinstance')
def create_book_instance(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = CreateBookInstanceForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            status = form.cleaned_data['status']

            book_instance = BookInstance.objects.create(book=book, status=status)
            book_instance.save()
            return HttpResponseRedirect(reverse('book-detail', kwargs={'pk': pk}))    

    return render(request, 'catalog/bookinstance_add.html', {'form': form, 'book': book})

@login_required
# @permission_required('catalog.add_user')
def create_new_user(request):
    form = CreateUserForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
                        
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            is_staff = form.cleaned_data['is_staff']
            password = form.cleaned_data['password']
            # confirm_password = form.cleaned_data['confirm_password']

            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_staff=is_staff)
            user.save()

            if is_staff == 't':
                assign_perm('auth.add_user', user)
                assign_perm('auth.change_user', user)
                assign_perm('auth.delete_user', user)
                assign_perm('catalog.add_book', user)
                assign_perm('catalog.change_book', user)
                assign_perm('catalog.delete_book', user)
                assign_perm('catalog.add_author', user)
                assign_perm('catalog.change_author', user)
                assign_perm('catalog.delete_author', user)
                assign_perm('catalog.add_bookinstance', user)
                assign_perm('catalog.change_bookinstance', user)
                assign_perm('catalog.delete_bookinstance', user)
                assign_perm('catalog.add_transaction', user)
                assign_perm('catalog.change_transaction', user)
                assign_perm('catalog.delete_transaction', user)
                assign_perm('catalog.view_transactions', user)
            else:
                assign_perm('catalog.view_transactions_by_user', user)
            
            assign_perm('catalog.view_book_detail', user)
            assign_perm('catalog.view_author_detail', user)
                

            return HttpResponseRedirect(reverse('users'))
        
    return render(request, 'catalog/create_user.html', {'form': form})

@login_required
@permission_required('catalog.add_bookinstance')
def update_book_status(request, pk):
    form = UpdateBookStatusForm(request.POST or None)
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        if form.is_valid():
            new_status = form.cleaned_data['new_status']

            book_instance.status = new_status
            book_instance.save()
            return HttpResponseRedirect(reverse('book-detail', kwargs={'pk': book_instance.book.id}))    

    return render(request, 'catalog/update_book_status.html', {'form': form, 'book_instance': book_instance})

def search_book(request):
    if request.method == 'GET':
        keyword = request.GET['book_keyword']
        cursor = connection.cursor()
        cursor.execute("SELECT b.id, b.title, a.first_name, a.last_name FROM catalog_book AS b, catalog_author AS a WHERE UPPER(b.title) LIKE UPPER(%s) AND b.author_id = a.id", ['%'+keyword+'%'])
        books = cursor.fetchall()
        data = []
        for row in books:
            dict_book = {}
            dict_book["pk"] = row[0]
            dict_book["title"] = row[1]
            dict_book["author"] = row[3] + ", " + row[2]
            data.append(dict_book)
        data = json.dumps(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, "catalog/book_list.html")

def search_author(request):
    if request.method == 'GET':
        keyword = request.GET['author_term']
        #authors = Author.objects.filter(first_name__icontains=keyword)
        #authors = serialize('json', authors)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM catalog_author WHERE UPPER(first_name) LIKE UPPER(%s) OR UPPER(last_name) LIKE UPPER(%s)", ['%'+keyword+'%', '%'+keyword+'%'])
        authors = cursor.fetchall()

        data = []
        for row in authors:
            cursor.execute("SELECT title FROM catalog_book WHERE author_id = %s", [row[0]])
            books = cursor.fetchall()
            books_data = []
            for book in books:
                books_data.append(book[0])

            dict_author = {}
            dict_author["id"] = row[0]
            dict_author["name"] = row[2] + ", " + row[1]
            
            date_of_birth = row[3].strftime('%m/%d/%Y')
            date_of_death = row[4].strftime('%m/%d/%Y')

            dict_author["life_span"] = date_of_birth + " - " + date_of_death
            dict_author["books"] = books_data

            data.append(dict_author)

        data = json.dumps(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, "catalog/author_list.html")


def search_borrower(request):
    if request.method == 'GET':
        keyword = request.GET['borrower_term']
        borrowers = User.objects.filter(
            (Q(first_name__icontains=keyword) 
            | Q(last_name__icontains=keyword)
            | Q(username__icontains=keyword)
            | Q(email__icontains=keyword))
            & Q(is_staff=False)
        )
        data = serialize('json', borrowers)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, "catalog/borrower_list.html")

def search_librarian(request):
    if request.method == 'GET':
        keyword = request.GET['librarian_term']
        librarians = User.objects.filter(
            (Q(first_name__icontains=keyword) 
            | Q(last_name__icontains=keyword)
            | Q(username__icontains=keyword)
            | Q(email__icontains=keyword))
            & Q(is_staff=True)
        )
        data = serialize('json', librarians)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, "catalog/librarian_list.html")


class BorrowerListView(LoginRequiredMixin, generic.ListView):
    model = User
    # permission_required = 'catalog.view_users'
    context_object_name = 'user_list'
    queryset = User.objects.filter(is_staff=False).order_by('date_joined')
    template_name = 'catalog/borrower_list.html'
    paginate_by = 5


class LibrarianListView(LoginRequiredMixin, generic.ListView):
    model = User
    # permission_required = 'catalog.view_users'
    context_object_name = 'user_list'
    queryset = User.objects.filter(is_staff=True)
    template_name = 'catalog/librarian_list.html'
    paginate_by = 5

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    queryset = Book.objects.all()
    template_name = 'book_list.html'
    paginate_by = 10


class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Book
    permission_required = 'catalog.view_book_detail'
    template_name = 'catalog/book_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    queryset = Author.objects.all()
    template_name = 'author_list.html'
    paginate_by = 5


class AuthorDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Author
    permission_required = 'catalog.view_author_detail'
    template_name = 'catalog/author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Transaction
    permission_required = 'catalog.view_transactions_by_user'
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 5

    def get_queryset(self):
        return Transaction.objects.filter(borrower=self.request.user)


class TransactionsListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Transaction
    permission_required = 'catalog.view_transactions'
    template_name = 'catalog/transactions.html'
    paginate_by = 5

    def get_queryset(self):
        # cursor = connection.cursor()
        # query = "SELECT t.* FROM catalog_transaction as t, catalog_bookinstance as bi WHERE t.book_instance_id = bi.id AND bi.status = 'o';"
        # cursor.execute(query)
        # transaction_list =  cursor.fetchall()

        # return transaction_list
        return Transaction.objects.filter(date_returned__isnull=True)
        # return BookInstance.objects.all()


class TransactionHistoryListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Transaction
    permission_required = 'catalog.view_transactions'
    templete_name = 'catalog/transaction_history.html'
    paginate_by = 5

    def get_queryset(self):
        return Transaction.objects.all().order_by('date_borrowed')


class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, edit.CreateView):
    model = Author
    permission_required = 'catalog.add_author'
    fields = '__all__'
    #initial = {'date_of_death': '05/01/2018'}


class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, edit.UpdateView):
    model = Author
    permission_required = 'catalog.change_author'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
 

class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, edit.DeleteView):
    model = Author
    permission_required = 'catalog.delete_author'
    success_url = reverse_lazy('authors')


class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, edit.CreateView):
    model = Book
    permission_required = 'catalog.add_book'
    fields = '__all__'


class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, edit.UpdateView):
    model = Book
    permission_required = 'catalog.change_book'
    fields = '__all__'


class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, edit.DeleteView):
    model = Book
    permission_required = 'catalog.delete_book'
    success_url = reverse_lazy('books')
