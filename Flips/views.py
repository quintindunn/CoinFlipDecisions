from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def new_flip(request):
    return render(request, "Flips/new-flip.html")