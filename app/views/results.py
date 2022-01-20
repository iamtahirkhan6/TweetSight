from django.shortcuts import render

def results(request):
    context = {}
    return render(request, "results.html", context)