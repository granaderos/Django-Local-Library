from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import edit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from .models import Book
from .models import Author
from .models import BookInstance
from .models import Genre
from .models import Transaction
from .forms import RenewBookForm
from .forms import CreateTransactionForm
from .forms import ReturnBookForm

import datetime
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

#@permission_required('catalog.can_mark_returned')
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

def create_new_transaction(request):
    # trans = get_object_or_404(Transaction, pk=pk)
    form = CreateTransactionForm(request.POST)
    if request.method == 'POST':
        form = CreateTransactionForm(request.POST)
        if form.is_valid():
            book_instance = BookInstance.objects.get(id=form.cleaned_data['book'])
            book_instance.status = 'o'
            date_borrowed = form.cleaned_data['date_borrowed']
            due_date = form.cleaned_data['due_date']
            borrower = User.objects.get(id=form.cleaned_data['borrower'])
            trans = Transaction.objects.create(book_instance=book_instance, date_borrowed=date_borrowed, due_back=due_date, borrower=borrower)
            trans.save()
            book_instance.save()
            return HttpResponseRedirect(reverse('transactions'))

    return render(request, 'catalog/create_transaction.html', {'form': form})

def return_book(request, pk):
    trans = get_object_or_404(Transaction, pk=pk)
    book_instance = get_object_or_404(BookInstance, pk=trans.book_instance.id)
    form = ReturnBookForm(request.POST)

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

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    queryset = Book.objects.all()
    template_name = 'book_list.html'
    paginate_by = 5


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    queryset = Author.objects.all()
    template_name = 'author_list.html'
    paginate_by = 5


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = Transaction
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 5

    def get_queryset(self):
        return Transaction.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class TransactionsListView(LoginRequiredMixin, generic.ListView):
    model = Transaction
    template_name = 'catalog/transactions.html'
    paginate_by = 5

    def get_queryset(self):
        return Transaction.objects.filter(date_returned__isnull=True)
        # return BookInstance.objects.all()


class TransactionHistoryListView(LoginRequiredMixin, generic.ListView):
    model = Transaction
    templete_name = 'catalog/transaction_history.html'
    paginate_by = 5

    def get_queryset(self):
        return Transaction.objects.all().order_by('date_borrowed')


class AuthorCreate(LoginRequiredMixin, edit.CreateView):
    model = Author
    fields = '__all__'
    #initial = {'date_of_death': '05/01/2018'}


class AuthorUpdate(LoginRequiredMixin, edit.UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
 

class AuthorDelete(LoginRequiredMixin, edit.DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(LoginRequiredMixin, edit.CreateView):
    model = Book
    fields = '__all__'


class BookUpdate(LoginRequiredMixin, edit.UpdateView):
    model = Book
    fields = '__all__'


class BookDelete(LoginRequiredMixin, edit.DeleteView):
    model = Book
    success_url = reverse_lazy('books')
