from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import SchoolSignupView, ResetPassword, ChangePasswordByOTP, CustomTokenObtainPairView, SendMail, \
    razorpay_webhook, LogoutView, PasswordView

urlpatterns = [
    path('token/',
         CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('signup/school/', SchoolSignupView.as_view(), name="school_signup"),
    path('reset/password/', ResetPassword.as_view(), name="reset_password"),
    path('change/password/otp/', ChangePasswordByOTP.as_view(), name="changes_password_by_otp"),
    path("send/mail/", SendMail.as_view(), name="sendMail"),
    path("logout/", LogoutView.as_view(), name="sendMail"),
    path("update/password/", PasswordView.as_view(), name="update password"),
]
