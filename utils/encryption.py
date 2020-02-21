import hashlib
import os


def md5(s):
    m = hashlib.md5(s.encode('utf8'))
    return m.hexdigest()


def gen_token():
    token = hashlib.sha1(os.urandom(24)).hexdigest()
    return token


def certify_token(token):
    pass


if __name__ == '__main__':
    token_ = gen_token()
    print(token_)
