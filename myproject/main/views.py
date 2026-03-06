from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')

def ErrorView(request, exception):
    return render(request, 'main/error.html')
