from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),
    url(r'register$', views.register),
    url(r'login$', views.login),
    url(r'books$', views.book_display),
    url(r'books/add$', views.books_add),
    url(r'detail$', views.review_detail),
    url(r'(?P<id>\d+)/user$', views.user),
    url(r'added$', views.added),
    url(r'(?P<id>\d+)/delete_review$', views.delete_review),
    url(r'(?P<id>\d+)/book_show$', views.book_show),
    url(r'(?P<id>\d+)/book_review_add$', views.add_review),
    url(r'back$', views.back) 
]
