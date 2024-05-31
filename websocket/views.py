from django.shortcuts import render


def main(request, id):
    
    return render(request, 'main.html')