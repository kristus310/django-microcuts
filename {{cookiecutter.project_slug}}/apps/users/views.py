from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .forms import UsernameForm, EmailForm, DeleteAccountForm, AvatarForm
from .models import UserProfile


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    #user = request.user

    #context = {
    #
    #}

    return render(request, "users/profile.html")


@login_required
@require_http_methods(["GET", "POST"])
def settings(request: HttpRequest) -> HttpResponse:
    user = request.user
    user_profile, _ = UserProfile.objects.get_or_create(user=user)

    username_form = UsernameForm(instance=user)
    email_form = EmailForm(instance=user)
    avatar_form = AvatarForm(instance=user_profile)
    delete_form = DeleteAccountForm(user=user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "avatar":
            if "avatar" in request.FILES:
                avatar_form = AvatarForm(request.POST, request.FILES, instance=user_profile)
                if avatar_form.is_valid():
                    avatar_form.save()
                    messages.success(request, "Avatar updated successfully.")
                    return redirect("users:settings")
                else:
                    messages.error(request, avatar_form.errors["avatar"][0])
            else:
                messages.error(request, "Please pick an image file before clicking save.")

        elif action == "profile":
            username_form = UsernameForm(request.POST, instance=user)
            email_form = EmailForm(request.POST, instance=user)
            if username_form.is_valid() and email_form.is_valid():
                username_form.save()
                email_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect("users:settings")
            messages.error(request, "Please fix the errors below.")

        elif action == "preferences":
            # ADD PREFERENCES
            messages.success(request, "Preferences updated successfully.")
            return redirect("users:settings")

    context = {
        "username_form": username_form,
        "email_form": email_form,
        "avatar_form": avatar_form,
        "delete_form": delete_form,
    }
    return render(request, "users/settings.html", context)


@login_required
@require_http_methods(["POST"])
def delete_avatar(request):
    request.user.profile.delete_avatar()
    messages.success(request, "Avatar removed.")
    return redirect("users:settings")


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
    return redirect("users:settings")