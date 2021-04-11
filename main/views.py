from django.shortcuts import render
from django.http import HttpResponse
from .update_db import get_prices

def homepage(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    return render(request, "home/home_tmp.html", {})
    
def company_view(request, company="COALINDIA"):
    print(company)
    context={}
    context['df'] = get_prices(company)
    return render(request, 'graph/df.html', context)

def testing(request, year=2005):
    print(year)
    print("testing hit")
    html="<html>HTML of testing is hit  </html>"
    return HttpResponse(html)