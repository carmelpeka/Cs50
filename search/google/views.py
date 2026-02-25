from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"google/index.html")
def index1(request):
    return render(request,"google/index1.html")
def index2(request):
    return render(request,"google/index2.html")
def index3(request):
    return render(request,"google/index3.html")