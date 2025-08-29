from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'artoon2d_blog/home.html')