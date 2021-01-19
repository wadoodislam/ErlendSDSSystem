import hashlib


def md5hash(name, provider):
    hashed = str(name) + '-' + str(provider)
    return hashlib.md5(hashed.encode()).hexdigest()
