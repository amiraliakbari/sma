# -*- coding: utf-8 -*-
from django.contrib import admin
from sma.books.models import Book, Author, Publisher, BookType, Reading, BookCategory

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(BookType)
admin.site.register(Reading)
admin.site.register(BookCategory)
