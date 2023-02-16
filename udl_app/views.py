from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import UserProfileInfo
from django.contrib.auth.models import User


def index(request):
    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        return HttpResponseRedirect(reverse('user_profile_page', kwargs={'slug': user.userprofileinfo.slug}))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('user_profile_page', kwargs={'slug': user.userprofileinfo.slug})) # type: ignore
            else:
                return HttpResponse("Account not active")
        else:
            return HttpResponse("Invalid login details <a href=''>back</a>")
    else:
        return render(request, 'udl_app/index.html', {})


def register_view(request):
    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        return HttpResponseRedirect(reverse('user_profile_page', kwargs={'slug': user.userprofileinfo.slug}))

    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)
            login(request, user)
            mail_message = "Thanks for registering on UDL!\n" \
                           "Your details have been submitted successfully as follows:\n" \
                           "Username: " + user.username + "\nEmail: " + user.email + "\nAadhaar Id: " + str(user.userprofileinfo.aadhaar_id)  # type: ignore
            user.email_user('UDL Registration Successful!', mail_message, ) # type: ignore
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'udl_app/register_page.html', {'user_form': user_form,
                                                          'profile_form': profile_form,
                                                          'registered': registered
                                                          })


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


class UserDetailView(LoginRequiredMixin, DetailView):
    model = UserProfileInfo
    template_name = 'udl_app/user_profile_page.html'
