from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from random import choice

from . import util

class CreateForm(forms.Form):
    common={'class': 'form-control', 'style': 'margin-bottom:5px;margin-top:5px'}
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Page Title'}|common))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Page Content'}|common))

def create(request):
    return render(request, "encyclopedia/create.html",{
        "form": CreateForm()
    })

def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries(),})

def entry(request, title):
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
    query = request.GET.get('q')
    if query in util.list_entries():
        return HttpResponseRedirect(f"wiki/{query}")
    elif query != None:
        return render(request,"encyclopedia/search.html",{
            "query": query,
            "entries": [entry for entry in util.list_entries() if query.lower() in entry.lower()],})

def random(request):
    return HttpResponseRedirect(f"wiki/{choice(util.list_entries())}")
    
