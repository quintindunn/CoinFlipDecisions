import os.path
import uuid

import urllib.request
import json

from .models import User

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, get_user_model

from django.contrib.auth import views as auth_views
from django.conf import settings

from django.http import HttpResponseNotAllowed, HttpResponseBadRequest
auth_file = os.path.join(settings.BASE_DIR, "oauth", "google_oauth.json")

with open(auth_file, 'r') as f:
    google_oauth_data = json.load(f)

GOOGLE_OAUTH_URI = (f"https://accounts.google.com/o/oauth2/v2/auth"
                    f"?redirect_uri={google_oauth_data['web']['redirect_uris'][0]}"
                    f"&prompt=consent&response_type=code&client_id={google_oauth_data['web']['client_id']}"
                    f"&scope=https://www.googleapis.com/auth/userinfo.email+https://www.googleapis.com/auth/plus.me"
                    f"+https://www.googleapis.com/auth/userinfo.profile+&access_type=offline")


def get_user_data(token_data):
    """
    Gets the user's data from the Google API, i.e. email, Google ID
    :param token_data: Token obtained from OAuth flow
    :return: Dict with the user's data
    """
    url = "https://www.googleapis.com/userinfo/v2/me?access_token=" + token_data.get("access_token")

    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise RuntimeError("Request error: ", response.status, response.read().decode())
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError("Request error: ", e.code, e.read().decode())
    except urllib.error.URLError as e:
        raise RuntimeError("Request error: ", e.reason)


def sign_up_with_google(request):
    ctx = {
        "redirect_uri": GOOGLE_OAUTH_URI
    }
    return render(request=request, template_name="Users/google_oauth.html", context=ctx)


def google_oauth_handler(request):
    data = request.GET.dict()

    def url_builder():
        base_url = google_oauth_data['web']['token_uri'] + "?"
        setup = {
            "grant_type": "authorization_code",
            "code": data.get('code'),
            "client_id": google_oauth_data['web']['client_id'],
            "client_secret": google_oauth_data['web']['client_secret'],
            "redirect_uri": google_oauth_data['web']['redirect_uris'][0],
        }
        for param, val in setup.items():
            base_url += f"{param}={val}&"

        return base_url

    req = urllib.request.Request(url_builder(), method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            request_data = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError("Request error: ", e.code, e.read().decode())
    except urllib.error.URLError as e:
        raise RuntimeError("Request error: ", e.reason)

    user_data = get_user_data(request_data)
    user = get_user_model().objects.all().filter(google_id=user_data['id']).first()
    if user is None:
        new_user = get_user_model().objects.create_user(
            username=user_data['email'].split("@")[0],
            email=user_data['email'],
            password=str(uuid.uuid4()),
            google_id=user_data['id'],
        )
        new_user.save()
        login(request, new_user)
        user = new_user
    else:
        login(request, user)

    if not user.display_name:
        return redirect("set-display-name")

    return redirect("home")


def set_display_name(request):
    if request.method == "GET":
        return render(request, "Users/set-display-name.html")

    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=["GET", "POST"])

    name = json.loads(request.body).get("displayname")

    if not name or len(name) < 5:
        return HttpResponseBadRequest()

    users = User.objects.filter(display_name=name).count()
    valid = users == 0

    if not valid:
        return HttpResponse("Name already taken", status=409)

    request.user.display_name = name
    request.user.save()

    return redirect("home")


def check_display_name(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods="POST")

    data = json.loads(request.body)
    new_name = data.get("displayname")
    if not new_name:
        return HttpResponseBadRequest()

    users = User.objects.filter(display_name=new_name).count()
    valid = users == 0
    return HttpResponse(str(valid).lower())


def logout_user(request):
    if not request.user.is_authenticated:
        return redirect("home")

    logout(request)

    return redirect("home")

class LoginView(auth_views.LoginView):
    template_name = 'Users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "google_oauth_uri": GOOGLE_OAUTH_URI
        })
        return context
