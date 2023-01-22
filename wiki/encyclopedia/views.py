from django.shortcuts import render
import markdown
import random
from . import util
from django import forms

class NewPageForm(forms.Form):
    name = forms.CharField(label = "Name", widget = forms.TextInput(attrs = {"class":"form-control col-lg-3"}))
    text = forms.CharField(label = "Text", widget = forms.Textarea(attrs = {"class":"form-control col-lg-9"}))
    edit = forms.BooleanField(initial = False, widget = forms.HiddenInput, required = False)

def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):

    try:
        return render(request, "encyclopedia/entry.html", {
         "entry": markdown.markdown(util.get_entry(entry)), 
         "entrytitle": entry
         })

    except:    
        return render(request, "encyclopedia/notfound.html", {
         "entrytitle": entry
         })
    

        


def search(request):
    li = []
    search = request.GET.get('q')
    entries = util.list_entries()
    for entry in entries:

        if util.get_entry(search) != None:
             return render(request, "encyclopedia/entry.html", { 
              "entry": markdown.markdown(util.get_entry(search)),
              "entrytitle": search
               })


        elif search.upper() in entry.upper():
               li.append(entry)
               return render(request, 'encyclopedia/index.html',{
                "entries": li,
                "entrytitle": (f"With {search}")
                 })


    return render(request, "encyclopedia/notfound.html",{
            "entrytitle": search
             })
        

   
def newpage(request):
    
    if request.method == "GET":
        form = NewPageForm(request.GET)
        return render(request, "encyclopedia/newpage.html", {
            "form": form,
            "entrytitle": ("Create A New Page"),
            "Submit": ("Create Page")
        })

    else:
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["name"]
            content = form.cleaned_data["text"]
            if util.get_entry(title) == None or form.cleaned_data["edit"] == True:
               util.save_entry(title, content)
               return render(request, "encyclopedia/entry.html", {
                "entry": markdown.markdown(util.get_entry(title)),
                "entrytitle": title

               })

            elif util.get_entry(title) != None:
               return render(request, "encyclopedia/newpage.html",{
                "form": form,
                "error": True,
                "entry": title,
                "entrytitle": ("Create A New Page"),
                "Submit": ("Create Page")
               })

            

def randompage(request):
    rali = util.list_entries()
    entry = random.choice(rali)
    return render(request, "encyclopedia/entry.html",{
        "entry": markdown.markdown(util.get_entry(entry)), 
        "entrytitle": entry
    })



def edit(request, entry):
    form = NewPageForm()
    form.fields["name"].initial = entry
    form.fields["name"].widget = forms.HiddenInput()
    form.fields["text"].initial = util.get_entry(entry)
    form.fields["edit"].initial = True

    return render(request, "encyclopedia/newpage.html",{
        "form": form,
        "edit": form.fields["edit"].initial,
        "entrytitle": (f"Editing {entry}"),
        "Submit": ("Edit Page")

    })