import time
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer, CustomTokenObtainPairSerializer
from school.serializer import SchoolSerializer
from .models import OTP, User
from utilities.permissions import IsAdmin, IsSchool, IsStudent, IsSchoolOrStudent
from utilities.Constants import reset_email_title, reset_email_body
from utilities.AccountHelper import get_otp, is_valid_otp
from school.models import School
from django.core.mail import EmailMessage
from datetime import datetime, timedelta
from rest_framework_simplejwt.views import TokenObtainPairView
from utilities.email import get_email_template, get_otp_email
from django.template.loader import render_to_string
from celery import shared_task
from django.views.decorators.csrf import csrf_exempt
import razorpay


def is_request_is_valid(data):
    is_valid = True
    error_data = []
    if not data.get('registration_no'):
        error_data.append("registration_no required")
        is_valid = False
    if not data.get('board'):
        error_data.append("board required")
        is_valid = False
    if not data.get('password'):
        error_data.append("password required")
        is_valid = False
    if not data.get('email'):
        error_data.append("email required")
        is_valid = False
    if not data.get('name'):
        error_data.append("name required")
        is_valid = False
    if not data.get('address_line1'):
        error_data.append("address_line1 required")
        is_valid = False
    if not data.get('phone'):
        error_data.append("phone required")
        is_valid = False
    if not data.get('owner_phone'):
        error_data.append("owner_phone required")
        is_valid = False
    if not data.get('city'):
        error_data.append("city required")
        is_valid = False
    if not data.get('pincode'):
        error_data.append("pincode required")
        is_valid = False
    if not data.get('state'):
        error_data.append("state required")
        is_valid = False
    if not data.get('country'):
        error_data.append("country required")
        is_valid = False
    if not data.get('principle_name'):
        error_data.append("principle_name")
        is_valid = False
    return is_valid, error_data


@shared_task()
def send_mail(user_name, password, email, school):
    html_code = get_email_template(user_name, password, school)
    # html_template = 'path/to/message.html'

    message = EmailMessage("Thank You For Choosing Reportify", html_code, "support@reportify.in", [email])
    message.content_subtype = 'html'  # this is required because there is no plain text email message
    message.send()


def send_otp_mail(email, otp):
    html_code = get_otp_email(otp)
    # html_template = 'path/to/message.html'

    message = EmailMessage("Reportify: Your OTP for ResetPassword", html_code, "support@reportify.in", [email])
    message.content_subtype = 'html'  # this is required because there is no plain text email message
    message.send()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom TokenObtainPairView that uses the CustomTokenObtainPairSerializer
    """
    serializer_class = CustomTokenObtainPairSerializer


class SendMail(APIView):
    def post(self, request):
        send_mail.delay("user_name", "password", "ehsan@reportify.in", "school")
        return Response()


class SchoolSignupView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        # coping the request so , we could add some field into it
        # print("adaddsad")
        is_valid, error_data = is_request_is_valid(request.data)
        if not is_valid:
            return Response({
                "Success": False,
                'data': error_data},
                status=status.HTTP_400_BAD_REQUEST)
        # /print(type(request.data))
        request_data = request.data
        request_data._immutable = False
        request_data._mutable = True
        # print(request_data)
        if not request_data.get('registration_no') or not request_data.get('board'):
            return Response({
                "Success": False,
                'data': [{'Error': 'Registration and Board cant be empty'}]},
                status=status.HTTP_400_BAD_REQUEST)

        registration_no = request_data.get('registration_no').lower()
        board = request_data.get('board').lower()
        email = request_data.get('email', None)
        if not email:
            return Response({
                "Success": False,
                'data': [{'Error': 'Email cant be empty'}]},
                status=status.HTTP_400_BAD_REQUEST)
        user_name = f'{board}{registration_no}'
        # print(user_name)
        request_data['username'] = user_name
        # request_data['is_school'] = True
        # request_data['email'] = email
        request_data._mutable = True
        # print(request_data)
        serializer = UserSerializer(data=request_data,
                                    context={'username': user_name, 'is_school': True, 'email': email})
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.save()
            request_data['user'] = new_user.id
            school_serializer = SchoolSerializer(data=request_data)
            if school_serializer.is_valid():
                school = school_serializer.save()
                school.save()
                response_data = {
                    'username': user_name,
                    'Password': request.data.get('password'),
                }

                send_mail(user_name, request.data.get('password'),
                          request.data.get('email'), request.data.get('name'))
                return Response({"Success": True,
                                 "Data": [response_data]}, status=status.HTTP_201_CREATED)
            else:

                # if some required field is missing delete the created user
                new_user.delete()
                error_data = school_serializer.errors
                return Response({"Success": False,
                                 "Data": [error_data]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            error_data = serializer.errors
            return Response({"Success": False,
                             "Data": [error_data]}, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated, IsSchool, IsStudent]

    def patch(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('old_password')


class ChangePasswordByOTP(APIView):

    def patch(self, request):
        otp = request.data.get("otp", None)
        username = request.data.get('username', None)

        if username and User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
        else:
            return Response({"Success": False,
                             "Data": ["Please provide correct username"]}, status=status.HTTP_400_BAD_REQUEST)
        if not School.objects.filter(user=user).exists():
            return Response({
                "Success": False,
                'Data': [{'Error': 'please provide valid email'}]},
                status=status.HTTP_400_BAD_REQUEST)
        if not OTP.objects.filter(otp=otp, user=user).exists():
            return Response({
                "Success": False,
                'Data': [{'Error': 'Otp has been expired or Wrong'}]},
                status=status.HTTP_400_BAD_REQUEST)
        otp_object = OTP.objects.get(otp=otp, user=user)
        current_time = str(datetime.now()).split(".")[0]
        # print(otp_object.updated_at + timedelta(minutes=10))
        a = "sadsad"
        otp_time = str(otp_object.updated_at + timedelta(minutes=10)).split(".")[0]

        if not is_valid_otp(otp_time, current_time):
            return Response({
                "Success": False,
                'Data': [{'Error': 'Otp has been expired'}]}),

        new_password = request.data.get('new_password', None)
        confirm_password = request.data.get('confirm_password', None)
        if not new_password or not confirm_password or not new_password.__eq__(confirm_password):
            return Response({
                "Success": False,
                'Data': [{'Error': 'new password and confirm password should be same'}]},
                status=status.HTTP_400_BAD_REQUEST)
        user = School.objects.get(user=user).user
        user.set_password(new_password)
        user.save()
        otp_object.delete()
        return Response({
            "Success": True,
            'Data': [{'Data': 'Password has been changes'}]},
            status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        if username and User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
        else:
            return Response({"Success": False,
                             "Data": ["Please provide correct username"]}, status=status.HTTP_400_BAD_REQUEST)
        if not username or not School.objects.filter(user=user).exists():
            return Response({"Success": False,
                             "Data": ["Please provide correct username"]}, status=status.HTTP_201_CREATED)
        school = School.objects.get(user=user)
        user = school.user
        otp = get_otp()
        if OTP.objects.filter(user=user).exists():
            otp_object = OTP.objects.get(user=user)
        else:
            otp_object = OTP.objects.create(user=user, otp=otp)
        otp_object.otp = otp
        otp_object.save()
        send_otp_mail(
            user.email, str(otp))
        return Response({"Success": True,
                         "Data": ["OTP has been sent successfully"]}, status=status.HTTP_201_CREATED)


@csrf_exempt
def razorpay_webhook(request):
    # client = razorpay.Client(auth=("rzp_test_AjbcnFz7qCh6iF", "4EwfOZL1938w6Y92AdsoM0Gt"))

    if request.method == 'POST':
        # Get the CSRF token from the request
        print("hehee")
        # csrf_token = request.META.get('HTTP_X_CSRFTOKEN', '')
        #
        # # Verify the CSRF token
        # if not csrf_token:
        #     return HttpResponse(status=403)

        # Verify webhook authenticity
        webhook_secret = "monu9889@1"  # Set the webhook secret obtained from Razorpay
        client = razorpay.Client(auth=("rzp_test_AjbcnFz7qCh6iF", "4EwfOZL1938w6Y92AdsoM0Gt"))
        signature = request.headers.get("X-Razorpay-Signature")

        # try:
        #     client.utility.verify_webhook_signature(request.body.decode(), signature, webhook_secret)
        # except Exception as e:
        #     return HttpResponse(status=400)

        # Process webhook event
        # event = request.headers.get("X-Razorpay-Event-Id")
        # data = request.body.decode()
        DATA = {
            "amount": 100,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": "value3",
                "key2": "value2"
            }
        }
        data = client.order.create(data=DATA)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"Success": True,
                             "Data": "logout succesful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        user = request.user
        data = request.data
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({'error': 'New password and confirm password do not match.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
