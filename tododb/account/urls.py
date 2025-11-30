from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("signup/", views.CreateAccountAPIView.as_view(), name="singup"),
    path("logout/", views.LogoutView.as_view(), name="logout_view"),
    path("request-otp/", views.RequestResetOTPAPIView.as_view(), name="request_otp"),
    path("reset/", views.ResetPasswordAPIView.as_view(), name="reset_password"),
    path("delete/", views.DeleteMyAccountAPIView.as_view(), name="delete_my_account"),
    path("me/", views.AmIAuthenticated.as_view()),
]


urlpatterns += [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
