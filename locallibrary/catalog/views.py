from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
def index(request):
    """
        Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = (BookInstance.objects.filter(status='a').count())
    crime_books = Book.objects.filter(title__icontains='crime').count()
    genre_books = Book.objects.filter(genre__name__iexact="novel").count()

    num_authors=Author.objects.count()
    # переменной context
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'crime_books': crime_books,
        'genre_books': genre_books,
    }
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
        model = Book
        paginate_by = 4

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
        model = Author
        paginate_by = 5

class AuthorDetailView(generic.DetailView):
        model = Author
