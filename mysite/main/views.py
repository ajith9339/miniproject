from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Customer
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout , authenticate
from django.contrib import messages
from .forms import NewUserForm
from django.utils import timezone
import urllib.request
from textblob import TextBlob
import sys,tweepy
import matplotlib.pyplot as plt

# Create your views here.

import bs4 as bs
import urllib.request

def scrapper(urlstring):
    source = urllib.request.urlopen(urlstring).read()
    soup = bs.BeautifulSoup(source,'lxml')
    for paragraph in soup.find_all('p'):
        block = str(paragraph.text)
        if block == None:
            pass
        else:
            print(str(paragraph.text))


def homepage(request):
    return render(request = request,template_name='main/home.html',context = {"Customer": Customer.objects.all})

# def details(request,id):
#     return render(request = request,template_name='main/details.html',context = {"tut":Tutorial.objects.get(id=id)} )


def details(request,id):
    tut = Customer.objects.get(id=id)
    scrap_url = tut.Customer_link
    if tut.Customer_content == "":
        source = urllib.request.urlopen(scrap_url).read()
        soup = bs.BeautifulSoup(source,'lxml')
        txt = ""
        for paragraph in soup.find_all('p'):
            block = str(paragraph.text)
            if block == None:
                pass
            else:
                txt += (str(paragraph.text))

        tut.Customer_content = txt
        tut.save()


    return render(request = request,template_name='main/details.html',context = {"tut":Customer.objects.get(id=id)} )




def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.info(request, f"you are now logged in as {username}")            
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})


def logout_request(request):    
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")





def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request = request,
                  template_name = "main/login.html",
                  context={"form":form})
def chat(request):
    return render(request=request,
                  template_name="main/chat.html",
                  )


def analytics(request):
    custs = Customer.objects.all()

    consumer_key = 'f1xm8xUnX4mkVyE7xxKRtdE2C'
    consumer_secret = 'MpnN9mWg7Ch4nyPnr7UeJxXqlOX3sKllCcdtaGJBCD5Z0yD7in'
    access_token = '1252848215998660608-MEe1L9Pw5uVPYCUX2cwEDscToPJ8DL'
    access_token_secret = 'Wc5gqnVNTeO3ZYdoqXhk1eQzWad1ladY7lGC4oh1Kzcwy'

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)

    api = tweepy.API(auth)


    for names in custs:
        polarity = 0
        subjectivity =0
        Customer_name = str(names.Customer_name)
        public_tweets = api.search(Customer_name)
        print(Customer_name)
        for tweet in public_tweets:
            analysis=TextBlob(tweet.text)
            Sentiment=analysis.sentiment
            polarity += Sentiment.polarity
            subjectivity += Sentiment.subjectivity
            names.pol=polarity
            names.sub=subjectivity
            names.save()

    return render(request,template_name = "main/analytics.html",context={'custs':custs})


