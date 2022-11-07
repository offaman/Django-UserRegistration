from django.shortcuts import render
from django.http import HttpResponse
from accounts.forms import registerationForm, loginForm, deleteForm, deleteConfirmation, forgetForm, changepasswordForm
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from passlib.hash import pbkdf2_sha256
from rest_framework.response import Response
import uuid
from accounts.models import Account, authTokenModel
from accounts.emailsend import send_mail_after_registration, send_mail_for_account_deletion, send_mail_for_change_password
import jwt
import datetime
import time


def register(request):
    form_to_register = registerationForm()
    # if request.method == 'POST':
    #     form_to_register = registerationForm(request.POST)
    #     user_password = request.POST.get('password')
    #     user_email = request.POST.get('email')
    #     if is_user_already_exist(user_email):
    #         return HttpResponse("Email is already exist")
    #     if form_to_register.is_valid():
    #         encryptedPassword = pbkdf2_sha256.encrypt(user_password, rounds=12000, salt_size=32)
    #         userform = form_to_register.save(commit = False)
    #         userform.is_varified = False
    #         userform.password = encryptedPassword
    #         token = str(uuid.uuid4())
    #         userform.auth_token = token
    #         send_mail_after_registration(user_email, token)
    #         form_to_register.save()
    #     return HttpResponse("Verify email sended to registered email id")
    # return render(request, 'register.html',{'form':form_to_register})
    if request.method == 'POST':
        form_to_register = registerationForm(request.POST)
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')
        if is_user_already_exist(user_email):
            return HttpResponse(f"User with {user_email} already exist")
        if form_to_register.is_valid():
            encryptedPassword = pbkdf2_sha256.encrypt(user_password, rounds=12000, salt_size=32)
            user_data_to_save = form_to_register.save(commit=False)
            user_data_to_save.password = encryptedPassword
            time_of_registration = datetime.datetime.now()
            user_data_to_save.creation_time = time_of_registration
            token = str(uuid.uuid4())
            send_mail_after_registration(user_email, token)
            user_data_to_save.save()
            user_token = authTokenModel.objects.create(
                user = user_data_to_save,
                auth_token = token,
                publishing_time= time_of_registration
            )
            return HttpResponse("Verify email sended to registered email id")
    return render(request, 'register.html',{'form':form_to_register})

def login(request):
    form_to_login = loginForm()
    if request.method == 'POST':
        form_to_login = loginForm(request.POST)
        user_password = request.POST.get('password')
        user_email = request.POST.get('email')
        try:
            user_to_login = Account.objects.filter(email= user_email)
            if user_to_login[0].isAuthorized:
                if(pbkdf2_sha256.verify(user_password, user_to_login[0].password)):
                    payload ={
                    'email' : user_email
                    }
                    jwt_cookie_token = jwt.encode(payload, 'secret')
                    response = HttpResponse("Login Successfull")  
                    response.set_cookie('cookie', jwt_cookie_token)
                    return response
                else:
                    return HttpResponse("Wrong Email or password")
            else:
                return HttpResponse("User is not verified yet")
        except:
            return HttpResponse("Wrong credetials")

    if request.method == 'GET':
        token = request.COOKIES.get('cookie')
        if token:
            decoded_payload = jwt.decode(token,'secret', algorithms=['HS256'])
            return HttpResponse("Already logined")
    return render(request, 'login.html',{'form':form_to_login})


def delete(request):
    form_to_delete = deleteForm()
    if request.method == 'POST':
        user_email = request.POST.get('email')
        try:
            user_to_login = Account.objects.get(email=user_email)
            if user_to_login.isAuthorized:
                token = str(uuid.uuid4())
                authTokenModel.objects.create(
                user = user_to_login,
                auth_token = token,
                publishing_time=  datetime.datetime.now()
                )
                send_mail_for_account_deletion(user_email, token)
                return HttpResponse("Email sended to your registered mail id")
            else:
                return HttpResponse("User not authorized")
        except:
            return HttpResponse("Wrong email Id")
    return render(request, 'delete.html',{'form':form_to_delete})


def confirmdelete(request, auth_token):
    delete_info_form = deleteConfirmation()
    if request.method == 'POST':
        try:
            user_with_authToken_to_delete = authTokenModel.objects.get(auth_token=auth_token).user
            user_password = request.POST.get('password')
            if(pbkdf2_sha256.verify(user_password, user_with_authToken_to_delete.password)):
                user_with_authToken_to_delete.delete()
                return HttpResponse("account deleted")
            return HttpResponse("Wrong password")
        except:
            return HttpResponse("Link expired!...Try to generate new link")
    else:
        if authTokenModel.objects.filter(auth_token=auth_token):
            return render(request, 'confirmdelete.html', {'form':delete_info_form})
        else:
            return HttpResponse("Link expired!...Try to generate new link")


def forgetpassword(request):
    password_forget_form = forgetForm()
    if request.method == 'POST':
        user_email = request.POST.get('email')
        try:
            user_object_to_change_password = Account.objects.get(email=user_email)
            if user_object_to_change_password.isAuthorized:
                token = str(uuid.uuid4())
                authTokenModel.objects.create(
                user = user_object_to_change_password,
                auth_token = token,
                publishing_time=  datetime.datetime.now()
                )
                send_mail_for_change_password(user_email, token)
                return HttpResponse("Email sended with link to change password")
            else:
                return HttpResponse("User is not authorized yet")
        except:
            return HttpResponse("Wrong Email Id")
    return render(request, 'forget.html', {'form':password_forget_form})


def changepassword(request, auth_token):
    change_password_form = changepasswordForm()
    if request.method == 'POST':
        try:
            user_object = authTokenModel.objects.get(auth_token=auth_token).user
            new_password = request.POST.get('password')
            encryptedPassword = pbkdf2_sha256.encrypt(new_password, rounds=12000, salt_size=32)
            user_object.password = encryptedPassword
            user_object.save()
            authTokenModel.objects.get(auth_token=auth_token).delete()
            return HttpResponse("Changed successfully")
        except:
            return HttpResponse("Link expired!.. Try to generate new link")
    return render(request, 'change.html', {'form':change_password_form})

def logout(request):
    if request.method == 'GET':
        req = HttpResponse("Logout Successfully")
        req.delete_cookie('cookie')
        return req

def authlogin(request):
    if request.method == 'GET':
        token = request.COOKIES.get('cookie')
        try:
            decoded_payload = jwt.decode(token,'secret', algorithms=['HS256'])
        except:
            return HttpResponse("error")
        useremail = Account.objects.get(email = (decoded_payload.get('email'))).email
        return HttpResponse(useremail)


def verify(request , auth_token):
    # try:
    #     sendedtoken = Account.objects.filter(auth_token=auth_token).first()
    #     if sendedtoken:
    #         if sendedtoken.isAuthorized:
    #             return HttpResponse("already verified")
    #         sendedtoken.isAuthorized = True
    #         sendedtoken.save()
    #         return HttpResponse("Successfully activated")
    #     else:
    #         return HttpResponse("error")
    # except Exception as e:
    #     return HttpResponse("error")
    try:
        user_with_authToken = authTokenModel.objects.get(auth_token=auth_token).user
        user_with_authToken.isAuthorized = True
        user_with_authToken.save()
        authTokenModel.objects.get(auth_token=auth_token).delete()
        return HttpResponse("User verified successfully.... You can now login")
    except:
        return HttpResponse("Link expired, Try to generate new link")


def is_user_already_exist(user_email):
    if Account.objects.filter(email=user_email):
        return True
    else:
        return False



def delete_after_particular_minutes(request):
    while True:
        auth_objects_to_delete = authTokenModel.objects.filter(publishing_time__lte= (datetime.datetime.now() - datetime.timedelta(minutes=2)).time())
        if len(auth_objects_to_delete):
            for objects in auth_objects_to_delete:
                if objects.user.isAuthorized == False:
                    objects.user.delete()
                objects.delete()
            time.sleep(10)
        else:
            pass