import hashlib
import datetime
from decimal import Decimal
import base64
import math
from os import urandom as _urandom


class PasswordHasher:
    algorithm = "pbkdf2_sha256"
    iterations = 320000
    digest = hashlib.sha256
    salt_entropy = 128
    _PROTECTED_TYPES = (
        type(None),
        int,
        float,
        Decimal,
        datetime.datetime,
        datetime.date,
        datetime.time,
    )
    RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def force_bytes(self, s, encoding="utf-8", strings_only=False, errors="strict"):
        if isinstance(s, bytes):
            if encoding == "utf-8":
                return s
            else:
                return s.decode("utf-8", errors).encode(encoding, errors)
        if strings_only and isinstance(s, self._PROTECTED_TYPES):
            return s
        if isinstance(s, memoryview):
            return bytes(s)
        return str(s).encode(encoding, errors)

    def pbkdf2(self, password, salt, iterations, dklen=0, digest=None):
        if digest is None:
            digest = hashlib.sha256
        dklen = dklen or None
        password = self.force_bytes(password)
        salt = self.force_bytes(salt)
        return hashlib.pbkdf2_hmac(digest().name, password, salt, iterations, dklen)

    def encode(self, password, salt, iterations=None):
        iterations = iterations or self.iterations
        _hash = self.pbkdf2(password, salt, iterations, digest=self.digest)
        _hash = base64.b64encode(_hash).decode("ascii").strip()
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, _hash)

    @staticmethod
    def decode(encoded):
        algorithm, iterations, salt, _hash = encoded.split("$", 3)
        return {
            "algorithm": algorithm,
            "hash": hash,
            "iterations": int(iterations),
            "salt": salt,
        }

    def verify(self, password, encoded):
        decoded = self.decode(encoded)
        encoded_2 = self.encode(password, decoded["salt"], decoded["iterations"])
        return self.constant_time_compare(encoded, encoded_2)

    def constant_time_compare(self, val1, val2):
        return self.force_bytes(val1) == self.force_bytes(val2)

    def salt(self):
        char_count = math.ceil(self.salt_entropy / math.log2(len(self.RANDOM_STRING_CHARS)))
        return self.get_random_string(char_count, allowed_chars=self.RANDOM_STRING_CHARS)

    def get_random_string(self, length, allowed_chars=RANDOM_STRING_CHARS):
        return "".join(self.choice(allowed_chars) for _ in range(length))

    def choice(self, seq):
        return seq[self._randbelow(len(seq))]

    def _randbelow(self, n):
        if not n:
            return 0
        getrandbits = self.getrandbits
        k = n.bit_length()
        r = getrandbits(k)
        while r >= n:
            r = getrandbits(k)
        return r

    @staticmethod
    def getrandbits(k):
        numbytes = (k + 7) // 8
        x = int.from_bytes(_urandom(numbytes), 'big')
        return x >> (numbytes * 8 - k)
