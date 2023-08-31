from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from rest_framework import status, generics, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.forms import LoginForm, SignupForm
from accounts.models import CustomUser
from accounts import serializers
from accounts.serializers import CustomUserSerializer, UserRegistrationSerializer


# Create your views here.


# todo :  login


class OTPView(APIView):
    def get(self, request: Request):  # for giving phone number
        serializer = serializers.RequestOTPSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                otp = serializers.OTPRequest.objects.generate(data)
                return Response(data=serializers.RequestOPTResponseSerializer(otp).data)
            except Exception as e:
                return Response(data=serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):  # for verifying
        serializer = serializers.VerifyOTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data


#
# class UserRegistrationView(APIView):
#     def post(self, request, format=None):
#         serializer = UserRegistrationSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "User registered successfully"})
#         print(serializer.errors)
#         return Response(serializer.errors)
#
#     def get(self, request, format=None):
#         form = SignupForm()
#         return render(request, 'accounts/register.html', {'form': form})


class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class UserProfileAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
