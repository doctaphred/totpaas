import hmac
from dataclasses import dataclass


@dataclass
class OTPGenerator:
    """Time-based One-Time Password generator.

    See https://datatracker.ietf.org/doc/html/rfc2104
    See https://datatracker.ietf.org/doc/html/rfc4226
    See https://datatracker.ietf.org/doc/html/rfc6238

    >>> totp = OTPGenerator(b'')
    >>> totp(0)
    '328482'
    >>> totp(29)
    '328482'
    >>> totp(30)
    '812658'
    >>> totp(31)
    '812658'

    >>> totp(38378250)
    '123456'

    >>> OTPGenerator(b'', time_step=60).totp(60)
    '812658'

    >>> OTPGenerator(b'', digits=20).totp(30)
    '00000000001230812658'

    >>> OTPGenerator(b'', digest='sha256').totp(30)
    '007993'
    """
    key: bytes
    time_step: int = 30
    digits: int = 6
    digest: str = 'sha1'

    @classmethod
    def from_b32(cls, key: str, **kwargs):
        return cls(cls.decode(key), **kwargs)

    @staticmethod
    def decode(key: str) -> bytes:
        from base64 import b32decode
        padding = '=' * ((8 - len(key)) % 8)
        return b32decode(key + padding, casefold=True)

    def hotp(self, counter: int) -> str:
        """HMAC-based One-Time Password.

           HOTP(K,C) = Truncate(HMAC-SHA-1(K,C))

        See https://datatracker.ietf.org/doc/html/rfc4226#section-5
        """
        assert counter >= 0, counter
        hmac_result = self._hmac(counter)
        truncated = self._truncate(hmac_result)
        reduced = self._reduce(truncated)
        return reduced

    def _hmac(self, counter: int) -> bytes:
        return hmac.digest(
            key=self.key,
            msg=counter.to_bytes(8, 'big'),
            digest=self.digest)

    def _truncate(self, hmac_result: bytes) -> int:
        """
        From the RFC:

        "The purpose of the dynamic offset truncation technique is to
        extract a 4-byte dynamic binary code from a 160-bit (20-byte)
        HMAC-SHA-1 result."
        """
        # Use the low-order 4 bits of the final byte as an offset.
        offset = hmac_result[-1] & 0xf
        # Extract the 4-byte "dynamic binary code" at the offset.
        P = hmac_result[offset:offset+4]
        # Return the last 31 bits of P (mask off the leftmost bit).
        bin_code = int.from_bytes(P, 'big') & 0x7fffffff
        return bin_code

    def _reduce(self, code: int) -> str:
        """Convert a 4-byte "dynamic binary code" to base-10 digits."""
        str_code = str(code).zfill(self.digits)
        return str_code[-self.digits:]

    def counter(self, time: float) -> int:
        assert time >= 0, time
        return int(time / self.time_step)

    def totp(self, time: float) -> str:
        """Time-based One-Time Password.

        See https://datatracker.ietf.org/doc/html/rfc6238#section-4

        >>> from math import nextafter
        >>> just_started = nextafter(0, 1)
        >>> almost_there = nextafter(30, 0)

        >>> totp = OTPGenerator(b'')
        >>> assert totp(0) == totp(just_started) == totp(almost_there)
        >>> assert totp(almost_there) != totp(30)

        >>> totp2 = OTPGenerator(b'', time_step=60)
        >>> assert totp(0) == totp2(0) == totp2(30)
        >>> assert totp(30) == totp2(60)
        """
        return self.hotp(self.counter(time))

    __call__ = totp
