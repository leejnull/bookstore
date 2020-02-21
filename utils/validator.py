import re


def validate_username(username):
    return len(username) >= 3


def validate_pass(password):
    return len(password) > 0


def validate_phone(phone):
    res = re.match(r'^1[0-9]{10}$', phone)
    if res:
        return True
    else:
        return False


def validate_email(email):
    res = re.match(r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}', email)
    if res:
        return True
    else:
        return False
