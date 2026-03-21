from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # Option 1: Simple text response
    return HttpResponse("Hello NDANA DYNASTY is live!")

    # Option 2: If you want to use a template instead:
    # return render(request, "index.html")
