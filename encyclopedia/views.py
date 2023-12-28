from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse

from . import util

class CreateForm(forms.Form):
    query = forms.CharField(label="Search Encyclopedia")

def index(request):
    if request.method == "GET":
        query = request.GET.get('q')
        if query in util.list_entries():
            return HttpResponseRedirect(f"wiki/{query}")
        elif query != None:
            return search(request,query)
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries(),})

def entry(request, title):
    if request.method == "GET":
        query = request.GET.get('q')
        if query in util.list_entries():
            return HttpResponseRedirect(query)
        elif query != None:
            return search(request,query)
    page = util.get_entry(title)
    if(page == None):
        return render(request, "encyclopedia/notfound.html", {
        "title": title
    })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": page,
        })
    
def search(request,query):
    return render(request,"encyclopedia/search.html",{
        "query": query,
        "entries": [entry for entry in util.list_entries() if query.lower() in entry.lower()],
    })
    
