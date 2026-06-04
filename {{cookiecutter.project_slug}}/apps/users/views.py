from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from django.conf import settings

from .forms import DeleteAccountForm, AvatarForm
from .models import UserProfile


@login_required
@require_http_methods(["POST"])
def delete_avatar(request):
    request.user.profile.delete_avatar()
    messages.success(request, "Avatar removed.")
    return redirect("/")


@login_required
@require_http_methods(["POST"])
def delete_account(request: HttpRequest) -> HttpResponse:
    user = request.user
    form = DeleteAccountForm(request.POST, user=user)
    if form.is_valid():
        logout(request)
        user.delete()
        messages.success(request, "Your account has been permanently deleted.")
        return redirect("account_login")
    messages.error(request, "Incorrect password. Account was not deleted.")
    return redirect("/")