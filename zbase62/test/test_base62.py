#!/usr/bin/env python
#
# Copyright (c) 2002-2010 Zooko Wilcox-O'Hearn
# mailto:zooko@zooko.com
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this work to deal in this work without restriction (including the rights
# to use, modify, distribute, sublicense, and/or sell copies).
import os, sys
import random, unittest

IS_PY2 = sys.version_info[0] == 2
if not IS_PY2:
    unicode = str

def div_ceil(n, d):
    """
    The smallest integer k such that k*d >= n.
    """
    return int((n//d) + (n%d != 0))

from zbase62 import zbase62

def random_bytes(n):
    return os.urandom(n)

class T(unittest.TestCase):
    def _test_num_octets_that_encode_to_this_many_chars(self, chars, octets):
        assert zbase62.num_octets_that_encode_to_this_many_chars(chars) == octets, "%s != %s <- %s" % (octets, zbase62.num_octets_that_encode_to_this_many_chars(chars), chars)

    def _test_ende(self, bs):
        alphas=zbase62.b2a(bs)
        bs2=zbase62.a2b(alphas)
        assert bs2 == bs, "bs2: %s:%s, bs: %s:%s, alphas: %s:%s" % (len(bs2), repr(bs2), len(bs), repr(bs), len(alphas), repr(alphas))

    def test_num_octets_that_encode_to_this_many_chars(self):
        self._test_num_octets_that_encode_to_this_many_chars(2, 1)
        self._test_num_octets_that_encode_to_this_many_chars(3, 2)
        self._test_num_octets_that_encode_to_this_many_chars(5, 3)
        self._test_num_octets_that_encode_to_this_many_chars(6, 4)

    def test_empty(self):
        self._test_ende(b'')

    def test_ende_0x00(self):
        self._test_ende(b'\x00')

    def test_ende_0x01(self):
        self._test_ende(b'\x01')

    def test_ende_0x0100(self):
        self._test_ende(b'\x01\x00')

    def test_ende_0x000000(self):
        self._test_ende(b'\x00\x00\x00')

    def test_ende_0x010000(self):
        self._test_ende(b'\x01\x00\x00')

    def test_ende_randstr(self):
        self._test_ende(random_bytes(2 ** 4))

    def test_ende_longrandstr(self):
        self._test_ende(random_bytes(random.randrange(0, 2 ** 10)))

    def test_odd_sizes(self):
        for j in range(2**6):
            lib = random.randrange(1, 2**8)
            numos = div_ceil(lib, 8)
            bs = random_bytes(numos)
            # zero-out unused least-sig bits
            if lib%8:
                b=ord(bs[-1]) if IS_PY2 else bs[-1]
                b = b >> (8 - (lib%8))
                b = b << (8 - (lib%8))
                bs = bs[:-1] + (chr(b) if IS_PY2 else bytes([b]))
            asl = zbase62.b2a(bs)
            assert len(asl) == zbase62.num_chars_that_this_many_octets_encode_to(numos) # the size of the base-62 encoding must be just right
            bs2l = zbase62.a2b_l(asl, lib)
            assert len(bs2l) == numos # the size of the result must be just right
            assert bs == bs2l

    def test_invalid(self):
        # doesn't fail
        zbase62.a2b('~!~')

    def test_types(self):
        assert type(zbase62.a2b(u'x')) == bytes
        assert type(zbase62.a2b(b'x')) == bytes

        assert type(zbase62.b2a(u'x')) == unicode
        assert type(zbase62.b2a(b'x')) == unicode

if __name__ == "__main__":
    unittest.main()
























