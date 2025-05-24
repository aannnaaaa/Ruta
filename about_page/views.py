from django.shortcuts import render

def about_view(request):
    return render(request, 'about_page/about.html')

def routes_view(request):
    return render(request, 'about_page/routes.html')