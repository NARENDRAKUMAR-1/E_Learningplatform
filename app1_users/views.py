from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView

# //for authentications
from django.contrib.auth import authenticate, login, logout

# // forms
from app1_users.forms import UserForm, UserProfileInfoForm
# Create your views here.

def index1(request):
    # return HttpResponse("Welcome Page")

    return render(request, 'home.html')


def register(request):

    registered = False

    if(request.method=="POST"):
        user_form = UserForm(data = request.POST)
        profile_form =  UserProfileInfoForm(data = request.POST)

        if(user_form.is_valid() and profile_form.is_valid() ):
            user = user_form.save()
            user.save()

            profile = profile_form.save(commit = False)

            profile.user = user
            profile.save()

            # // all done
            registered = True

        else:
            print("user_form.errors, profile_form.errors")
    
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
        #  all these forms are coming from forms.py
        #  forms.py internally uses the models.py in their meta

    
    # //return as
    return render(request,
    'registration.html',
    {
        'registered' : registered,
        'user_form' : user_form,
        'profile_form' : profile_form
    })



def user_login(request):
    if(request.method == 'POST'):
        username =request.POST.get('username')
        password =request.POST.get('password')


        # //use inbuilt functionality for authentication
        user = authenticate(username = username, password=password)

        if user: # authenticated
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
                # index here is namespace for the homepage

            else:
                return HttpResponse("Account is Deactivated or Not available")

        else:
            return HttpResponse("Username or Password wrong please use the correct credentials")
    
    return render(request, 'login.html')


# @login_required #decorator by django
# check if user is logged out
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


