from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from random import choice

from . import util
common={'class': 'form-control'}   
class CreateForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Page Title'}|common))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Page Content (in markdown)'}|common))

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs=common))
    
    
def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title.lower() in [t.lower() for t in util.list_entries()]:
                return render(request, "encyclopedia/create.html",{"form": form,"invalid":True})
            else:
                util.save_entry(title=title,content=form.cleaned_data["content"])
                return HttpResponseRedirect(f"wiki/{title}")
        else:
            return render(request, "encyclopedia/create.html",{"form": form})
    else:
        return render(request, "encyclopedia/create.html",{"form": CreateForm()})

def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries(),})

def entry(request, title):
    page = util.entry2html(title)
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
    return render(request,"encyclopedia/search.html",{
            "query": query,
            "entries": [entry for entry in util.list_entries() if query.lower() in entry.lower()],})

def random(request):
    return HttpResponseRedirect(f"wiki/{choice(util.list_entries())}")

def edit(request,entry):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            util.save_entry(title=entry,content=form.cleaned_data["content"].replace("\r\n","\n"))
            return HttpResponseRedirect(f"../wiki/{entry}")
    else:
        return render(request,"encyclopedia/edit.html",{"title": entry,"form": EditForm(initial={'content': util.get_entry(entry)})})
    
