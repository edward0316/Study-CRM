from django.shortcuts import render, HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("<h1>111<h1>")


def aaa(request):
    return render(request, 'app02/index2.html')
