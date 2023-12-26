from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    page = util.get_entry(title)
    if(page == None):
        return render(request, "encyclopedia/notfound.html", {
        "title": title
    })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": page
        })
