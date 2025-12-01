from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
#from django.contrib.auth.decorators import login_required, permission_required
def index(request):
    """
        Функция отображения для домашней страницы сайта.
    """
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = (BookInstance.objects.filter(status='a').count())
    crime_books = Book.objects.filter(title__icontains='crime').count()
    genre_books = Book.objects.filter(genre__name__iexact="novel").count()
    # переменной context
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
        'crime_books': crime_books,
        'genre_books': genre_books,
    }
    return render(request, 'index.html', context=context)

class BookListView(LoginRequiredMixin, generic.ListView):
        model = Book
        paginate_by = 4

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

class AuthorListView(LoginRequiredMixin, generic.ListView):
        model = Author
        paginate_by = 5

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
        model = Author



class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )


class LibrarianBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_librarian.html'
    paginate_by = 10

    # Это применяет требование разрешения ко всему представлению
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')