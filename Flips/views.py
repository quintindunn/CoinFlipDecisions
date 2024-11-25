from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseBadRequest

from .models import Flip


@login_required()
def new_flip(request):
    if request.method == "GET":
        return render(request, "Flips/new-flip.html")

    post_data = request.POST
    option_a_label: str = post_data.get("option-a")
    option_b_label: str = post_data.get("option-b")
    weighting: str | int | float = post_data.get("weighting")
    private: str | bool = post_data.get("private")

    # Validation
    if len(option_a_label) > 128 or option_a_label == "":
        return HttpResponseBadRequest()

    if len(option_b_label) > 128 or option_b_label == "":
        return HttpResponseBadRequest()

    if not weighting.isalnum():
        return HttpResponseBadRequest()

    weighting = int(weighting)

    if weighting not in range(1, 100):
        return HttpResponseBadRequest()

    if private not in ("true", None):
        return HttpResponseBadRequest()

    weighting = weighting / 100
    private = private == "true"

    flip = Flip(option_a=option_a_label, option_b=option_b_label, option_a_weight=1-weighting,
                option_b_weight=weighting, private=private, user=request.user)
    flip.save()

    return render(request, "Flips/new-flip.html")
