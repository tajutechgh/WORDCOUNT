# pylint: disable=missing-module-docstring
from re import template
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth 
from django.contrib import messages
from .models import WordCount
from django.template import loader
from django.core.mail import EmailMultiAlternatives

def index(request):

    return render(request, 'index.html')

def counter(request):
    
    wordCount = WordCount()

    wordCount.text = request.POST['text']

    wordCount.save()
    
    text = request.POST['text']

    amount_of_words = len(text.split())

    return render(request, 'counter.html', {'words_count': amount_of_words})

def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(username=username).exists():

            messages.info(request, 'Username provided is already in use!')

            return redirect('register')

        elif User.objects.filter(email=email).exists():

            messages.info(request, 'Email provided is already in use!')

            return redirect('register')

        else:

            if password == confirm_password:
                
                user = User.objects.create(username=username, email=email, password=password)

                user.save()
                
                #to send an email notification 
                template = loader.get_template('contact_form.txt')
                
                context = {
                    'username': username,
                    'email': email,
                }
                
                message = template.render(context)
                
                email = EmailMultiAlternatives(
                    "Registration Test", message,
                    "Congratulations" + "- A gift to you",
                    ['jakuraaziz@gmail.com', email]
                )
                
                #convert the html and css inside the [contact_form.txt] to html template
                email.content_subtype = 'html'
                
                email.send()
                
                messages.success(request, 'Please kindly check your email to confirm your registration!')

                return redirect('login')

            else:

                messages.info(request, 'Your passwords do not match!')

                return redirect('register')

    return render(request, 'register.html')

def login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:

            auth.login(request, user)

            return redirect('/')

        else:

            messages.info(request, 'Your credentials do not match!')

            return redirect('login')

    else:

        return render(request, 'login.html')

def logout(request):

    auth.logout(request)

    return redirect('/')

def post(request, pk):

    return render(request, 'post.html', {'pk': pk})