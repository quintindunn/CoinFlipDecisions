import json
import random

from Core.decorators import check_display_name

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponseForbidden

from .models import Flip


@check_display_name
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

    flip = Flip(option_a=option_a_label, option_b=option_b_label, option_a_weight=1 - weighting,
                option_b_weight=weighting, private=private, user=request.user, disabled=False)
    flip.save()

    return redirect("execute-flip", pk=flip.uuid)


@check_display_name
def execute_flip(request, pk: str):
    flip = Flip.objects.filter(uuid=pk, disabled=False).first()

    if flip is None:
        return HttpResponseNotFound()

    if flip.private and (not request.user.is_authenticated or request.user != flip.user):
        return HttpResponseForbidden()

    ctx = {
        "is_owner": flip.user == request.user,
        "flip": flip,
        "first_flip": False,
        "heads_chance": f"{int(flip.option_a_weight * 100)}%",
        "tails_chance": f"{int(flip.option_b_weight * 100)}%"
    }

    # Process it server-side to prevent people from making false HTTP requests
    if flip.outcome == 0:
        flip.outcome = int(random.random() > flip.option_a_weight) + 1  # 0 == not processed, 1 == Heads 2, == Tails
        flip.save()
        ctx["first_flip"] = True

    return render(request, "Flips/execute-flip.html", context=ctx)


# TODO: VALIDATION
def rate(request):
    request_data = json.loads(request.body)

    uuid = request_data.get("flip-id")
    value = request_data.get("value")

    flip = request.user.flips.filter(uuid=uuid, disabled=False).first()

    if not flip:
        return HttpResponseNotFound()

    if flip.user != request.user:
        return HttpResponseForbidden()

    flip.outcome_rating = value
    flip.save()
    return HttpResponse("OK", status=200)


def update_visibility(request):
    request_data = json.loads(request.body)

    uuid = request_data.get("flip-id")

    flip = request.user.flips.filter(uuid=uuid, disabled=False).first()

    if not flip:
        return HttpResponseNotFound()

    if flip.user != request.user:
        return HttpResponseForbidden()

    private = request_data.get("set_private")
    remove = request_data.get("remove")

    flip.private = private
    flip.disabled = remove
    flip.save()

    return HttpResponse("OK", status=200)


@check_display_name
def my_flips(request):
    flips = request.user.flips.filter(disabled=False)
    ctx = {
        "flips": flips[::-1]
    }
    return render(request, "Flips/my-flips.html", context=ctx)
