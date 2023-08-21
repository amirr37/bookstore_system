from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.forms import LoginForm, SignupForm, CustomUserCreationForm
from accounts.models import CustomUser
from accounts.serializers import UserRegistrationSerializer


# Create your views here.


# todo :  signup - profile -


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"})
        print(serializer.errors)
        return Response(serializer.errors)

    def get(self, request, format=None):
        form = CustomUserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        print("yek")
        logout(request)
        print("222")
        return redirect('login')


class LoginView(APIView):
    def get(self, request: Request):
        # todo : fix if statement
        if request.user.is_authenticated:
            return redirect('book-list')
        context = {'login_form': LoginForm()}
        return render(request, 'accounts/login.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('index')

        login_form = LoginForm(request.data)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return redirect('index')
                # return Response({'access_token': access_token})
            else:
                login_form.add_error('username', 'invalid username or password')
                return render(request, 'accounts/login.html',
                              {'login_form': login_form, })
        else:
            login_form.add_error('username', 'invalid username or password')
            return render(request, 'accounts/login.html', {'login_form': login_form})


class IndexPageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/index.html'

# class SignupView(View):
#     def get(self, request):
#         context = {'signup_form': SignupForm}
#         return render(request, 'accounts/register.html', context)
#
#     def post(self, request):
#         signup_form = SignupForm(request.POST)
#         if signup_form.is_valid():
#             username = signup_form.cleaned_data['username']
#             email = signup_form.cleaned_data['email']
#             fname = signup_form.cleaned_data['first_name']
#             lname = signup_form.cleaned_data['last_name']
#
#             password = signup_form.cleaned_data['password']
#
#             # Check if a user with the same username already exists
#             if CustomUser.objects.filter(username=username).exists():
#                 signup_form.add_error('username', 'Username already exists')
#                 context = {'signup_form': signup_form}
#                 return render(request, 'accounts/register.html', context)
#
#             # Create a new user object
#             new_user = CustomUser(username=username, email=email, first_name=fname, last_name=lname)
#
#             # Set the password for the new user
#             new_user.set_password(password)
#
#             # Save the new user to the database
#             new_user.save()
#
#             # Redirect the user to a success page or login page
#             return redirect('login')
#
#         # If the form is not valid, re-render the signup page with the form and error messages
#         context = {'signup_form': signup_form}
#         return render(request, 'accounts/register.html', context)
