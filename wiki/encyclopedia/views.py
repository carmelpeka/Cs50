from django.shortcuts import render
import markdown
from . import util
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
import random
from django.http import HttpResponse

from django import forms
# Create your views here.
entries=util.list_entries()
class NewTaskForm(forms.Form):
    q=forms.CharField(label="New Task")

class NewTaskForm1(forms.Form):
    title = forms.CharField(label="Titre")
    content = forms.CharField(widget=forms.Textarea)

def index(request):

    if request.method == "GET":
        form = NewTaskForm(request.GET)
        if form.is_valid():
            task = form.cleaned_data["q"]

            entries=util.list_entries()
            result = [entry for entry in entries if task in entry]

            if task and task in entries:
               return redirect("title", title=task)
            elif len(result)>0:
               return redirect("resultat",task)
            else:
               return HttpResponse(f"Erreur : {task} not exits.")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):

    entry = util.get_entry(title)

    if entry is not None:
        html = markdown.markdown(entry)
    else:
        html = None

    return render(request, "encyclopedia/title.html", {
           "markdown": html,
           "title": title
           })

def resultat(request,task):

        result = [entry for entry in entries if task in entry]
        return render(request, "encyclopedia/resultat.html", {
           "entries": result

           })


def savearticle(request):
    if request.method=="POST":
        form = NewTaskForm1(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()
            if title in entries:
                return HttpResponse(f"Erreur : {title} already exits.")

            else:
                util.save_entry(title, content)
                return render(request, "encyclopedia/title.html", {
                    "markdown": content,
                    "title": title
                })

    return render(request, "encyclopedia/savearticle.html"

    )
def modifytransition(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["q"]

            return redirect("modify",title=title)
    return render(request, "encyclopedia/modifytransition.html")
def modify(request,title):
    content=util.get_entry(title)
    if request.method=="POST":
        form = NewTaskForm1(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/title.html", {
                "markdown":content,
                "title": title

            })

    return render(request, "encyclopedia/modify.html", {
        "markdown": content,
        "title":title

    })
def randompage(request):

    entries = util.list_entries()

    title = random.choice(entries)

    return redirect("title", title=title)

