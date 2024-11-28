from django.shortcuts import render
from Flips.models import Flip


def home(request):
    recent_flips = Flip.objects.filter(private=False, disabled=False).order_by('-id')[:10]
    ctx = {
        "flips": recent_flips
    }
    return render(request, "home/home.html", context=ctx)