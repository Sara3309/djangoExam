from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
import datetime
from django.db.models import Count

def index(request):
    request.session.clear()
    if 'user' not in request.session:
        request.session['user'] = None
    return render(request,"belt_review/login.html")

def register(request):
    request.session.clear()
    errors = User.objects.basic_validator(request.POST)
    
    if len(errors):
        for key,value in errors.items():
            messages.error(request,value, extra_tags="register_error:"+str(key))
        return redirect("/")

    else:
        user = User.objects.create()
        user.first_name = request.POST['first_name']
        user.last_name= request.POST['last_name']
        user.email = request.POST['email']
        hash1 = bcrypt.hashpw(request.POST['code'].encode(), bcrypt.gensalt())
        user.password = hash1
        
        user.save()
        request.session['user'] = user.first_name
        request.session['id']= user.id
        messages.success(request, "User successfully added.")
        return redirect("/books")

def login(request):
    request.session.clear()
    if len(request.POST['email2']) < 1:
        messages.error(request, "Email cannot be blank.", extra_tags='suggest_email')
    if len(request.POST['code2']) < 1:
        messages.error(request,"Password cannot be blank", extra_tags="suggest_pw")
    if len(request.POST['email2']) > 1 and len(request.POST['code2']) > 0:

        if User.objects.filter(email=request.POST['email2']):
            user = User.objects.filter(email=request.POST['email2'])
            
            if bcrypt.checkpw(request.POST['code2'].encode(), user[0].password.encode()):
                request.session['user'] = user[0].first_name
                request.session['id'] = user[0].id
                return redirect("/books")
            else:
                messages.error(request,'Wrong Password', extra_tags='suggest_pw')
                return redirect("/")
        else:
            messages.error(request,'User does not exist, please register', extra_tags='suggest_email')
            return redirect("/")
    return redirect("/")


def back(request):
    request.session.clear()
    return redirect("/")

def book_display(request):
    reviews=Review.objects.order_by('-created_at').all()[:3]
    tempBook = Review.objects.order_by('-created_at').all()
    books = []
    book_titles = []
    for i in tempBook:
        if (i.book_reviewed.title not in book_titles):
            books.append(i)
            book_titles.append(i.book_reviewed.title)

    context={
        "reviews":reviews,
        "books": books,
        "ratings" : [0,1,2,3,4]
    }
    
    return render(request,"belt_review/book_display.html",context)

def books_add(request):
    if "id" in request.session:
        return render(request,"belt_review/review_add.html")
       
def added(request):
    error = False
    if len(request.POST['title']) < 1:
        messages.error(request, "Book title cannot be blank.", extra_tags='title')
        error = True
        print("1"*50)
    if request.POST['author'] =="" or len(request.POST['new_author'])<1:
        messages.error(request, "Please fill in the author or choose one.", extra_tags='author')
        print("2"*50)
        error = True
    if len(request.POST['content']) <1:
        messages.error(request, "Please fill in review.", extra_tags='review')
        print("3"*50)
        error = True
    elif Book.objects.filter(title=request.POST['title']):
        messages.error(request, "Book already exist.", extra_tags='title')
        print("4"*50)
        error = True
    

    if error:
        return redirect("/books/add")

    if request.method=="POST":
        user=User.objects.get(id=request.session['id'])
        author=request.POST['author'] or request.POST['new_author']
        new_book=Book.objects.create(title=request.POST['title'],author=author)
        new_review=Review.objects.create(content=request.POST['content'],rating=int(request.POST['star']),review_poster=user,book_reviewed=new_book)
        request.session['book_id']=new_book.id
        request.session['review_id']=new_review.id
        request.session['book_title']=new_book.title
        request.session['book_author']=new_book.author
        request.session['review_content']=new_review.content
        request.session['time']=str(new_review.created_at)
        request.session['rating']=str(new_review.rating)
            
        
        return redirect("/review_detail")
    
def review_detail(request):
   
    reviews=Review.objects.filter(book_reviewed=Book.objects.get(title=request.session['book_title'])).all()
    context={
        "reviews":reviews,
        "book_id":Book.objects.get(title=request.session['book_title']),
        "ratings" : [0,1,2,3,4]
    }
   
    return render(request,"belt_review/review_detail.html",context)

def add_review(request,id):
    if len(request.POST['book_content'])<1:
        messages.error(request, "Book title cannot be blank.", extra_tags='book_review')
        return redirect("/review_detail")
    else:
        user=User.objects.get(id=request.session['id'])
        book=Book.objects.get(id=id)
        Review.objects.create(content=request.POST['book_content'],rating=request.POST['star1'], review_poster=user,book_reviewed=book)
        return redirect("/review_detail")
def user(request,id):
    tempBook = Review.objects.order_by('-created_at').all()
    books = []
    book_titles = []
    for i in tempBook:
        if (i.book_reviewed.title not in book_titles):
            books.append(i)
            book_titles.append(i.book_reviewed.title)
    context={
        "first_name":User.objects.get(id=id).first_name,
        "full_name":User.objects.get(id=id).first_name+" "+User.objects.get(id=id).last_name,
        "email": User.objects.get(id=id).email,
        "total_reviews": Review.objects.filter(review_poster=id).count(),
        "books": books
    }
    return render(request,"belt_review/user.html",context)

def book_show(request,id):
    book=Book.objects.get(id=id)
    request.session['book_title'] =book.title
    request.session['book_author'] =book.author
    return redirect("/review_detail")

def delete_review(request,id):
    b=Review.objects.get(id=id)
    b.delete()

    return redirect("/review_detail")
