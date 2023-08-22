from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.forms import LoginForm, SignupForm, CustomUserCreationForm
from accounts.models import CustomUser
from accounts.serializers import UserRegistrationSerializer, RequestOTPSerializer, OTPRequest, \
    RequestOPTResponseSerializer


# Create your views here.


# todo :  login


class OTPView(APIView):
    def get(self, request: Request):  # for giving phone number
        serializer = RequestOTPSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                otp = OTPRequest.objects.generate(data)
                return Response(data=RequestOPTResponseSerializer(otp).data)
            except Exception as e:
                return Response(data=serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def post(self, request):  # for verifying
            pass


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


class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        # return self.model.objects.get(username=self.request.user.username)
        return self.request.user
