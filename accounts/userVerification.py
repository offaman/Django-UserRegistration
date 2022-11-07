from accounts.models import Account

def is_user_authorized(user_email):
    if Account.objects.filter(email= user_email):
        return True
    else:
        return False