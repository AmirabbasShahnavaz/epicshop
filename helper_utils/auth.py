from django.http import HttpRequest


def check_user_authenticated(request : HttpRequest):
    if request.user.is_authenticated:
        return True
    else:
        return False

def get_mobile_show(mobile:str):
    return f'09xxxxxx{mobile[9:12]}'