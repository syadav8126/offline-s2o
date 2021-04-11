from django.shortcuts import render
from django.http import HttpResponse

def homepage(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    return render(request, "home/home_tmp.html", {})

def testing(request, year=2005):
    print(year)
    print("testing hit")
    html="<html>HTML of testing is hit  </html>"
    return HttpResponse(html)