# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserAccountSerializer, ResetPasswordSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
import random, hashlib
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from core.models import RequestedOtp
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken, TokenError


User = get_user_model()


class CreateAccountAPIView(APIView):
    """View to create  new account for the user"""

    authentication_classes = []
    permission_classes = []

    def get(self, request):

        return Response({"message": "hello"}, status=status.HTTP_200_OK)

    def post(self, request):

        serializer = UserAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "user created ",
            },
            status=status.HTTP_200_OK,
        )

        # Create your views here.


class LoginAPIView(APIView):
    """APIView is manage the login enpont"""

    authentication_classes = []
    permission_classes = []

    def get(self, request):

        return Response({"message": "hello"}, status=status.HTTP_200_OK)

    def post(self, request):

        serializer = UserAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        print(email, password)

        user = authenticate(request, username=email, password=password)
        if user is not None:
            # now we will generate token for the user no session
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Wrong credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

        except TokenError:
            return Response(
                {"error": "Token is invalid or expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception:
            return Response(
                {"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )


class RequestResetOTPAPIView(APIView):
    """View handle user validation create and delete previous otp request objects"""

    authentication_classes = []
    permission_classes = []

    def get(self, request):

        return Response({"message": "hello"}, status=status.HTTP_200_OK)

    def post(self, request):

        email = request.data.get("email")
        print(email)
        try:
            user = User.objects.get(email=email)

            random_number = random.randrange(1111, 9999)
            hased_text = hashlib.sha256(str(random_number).encode()).hexdigest()
            # before creating new oject in database we will delete all previous otp requests objects
            RequestedOtp.objects.filter(user=user).all().delete()

            # create object of the otp hased value with request email
            RequestedOtp.objects.create(user=user, hashed_text=hased_text)
            # sedning email to user mail
            send_mail(
                subject="Hey this is below is the otp to reset your password ",
                message=f"{random_number}",
                from_email="dinesh@gmail.com",
                recipient_list=[user.email],
            )

        except User.DoesNotExist or Exception as e:
            print("ther is some errror ")
        ## returning a general message either the user exits or not exits.
        return Response(
            {
                "message": "A 4-digit verification code has been sent to your registered email address."
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        otp = serializer.validated_data["otp"]

        print(email, password, otp)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {"message": "No account found with this email"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # hash the otp received
        hashed_text = hashlib.sha256(str(otp).encode()).hexdigest()

        otp_obj = RequestedOtp.objects.filter(
            user=user, hashed_text=hashed_text, expire_time__gt=timezone.now()  # FIXED
        ).first()

        if not otp_obj:
            return Response(
                {"message": "Invalid or expired OTP"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If OTP is valid
        user.set_password(password)
        user.save()
        otp_obj.delete()

        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_200_OK,
        )


class DeleteMyAccountAPIView(APIView):
    """view to handle the account deletion of hte user with the all task created by the user"""

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({"message": "hello"}, status=status.HTTP_200_OK)

    def post(self, request):

        User.objects.filter(email=request.user.email).delete()

        return Response(
            {"message": "user account delete with all its task's "},
            status=status.HTTP_200_OK,
        )


class CheckAuth(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        print(request.headers)
        print(request.headers.get("authorization", None))
        print("we are in the get method ")

        return Response({"mesage": "ok"}, status=status.HTTP_200_OK)
