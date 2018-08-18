#!/usr/bin/env python
import secrets
import string

from passlib.hash import sha512_crypt


def crypt(password, salt=None, rounds=5000):
    random = secrets.SystemRandom()
    if salt is None:
        salt = ''.join(random.choices(string.digits + string.ascii_letters, k=16))
    return sha512_crypt.hash(password, salt=salt, rounds=rounds)
