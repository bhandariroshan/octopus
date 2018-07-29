import hashlib, uuid


class WordHasher(object):
    @staticmethod
    def hash(word, salt='roshan'):
        string = word + salt
        hash = str(hashlib.sha512(string.encode('utf-8')).hexdigest())
        return hash