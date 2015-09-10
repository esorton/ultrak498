##############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Eric F Sorton
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
##############################################################################

import unittest
import ultrak498

class TEST_bcd_to_int(unittest.TestCase):
    def testValueOfZeroReturnsZero(self):
        value = ultrak498.bcd_to_int(chr(0x00))
        self.assertEqual(value, 0)

    def testValueOfOneReturnsOne(self):
        value = ultrak498.bcd_to_int(chr(0x10))
        self.assertEqual(value, 1)

    def testValueOfNineReturnsNine(self):
        value = ultrak498.bcd_to_int(chr(0x90))
        self.assertEqual(value, 9)

    def testValueOfTenReturnsTen(self):
        value = ultrak498.bcd_to_int(chr(0x01))
        self.assertEqual(value, 10)

    def testValueOfElevenReturnsEleven(self):
        value = ultrak498.bcd_to_int(chr(0x11))
        self.assertEqual(value, 11)

    def testValueOfFifteenReturnsFifteen(self):
        value = ultrak498.bcd_to_int(chr(0x51))
        self.assertEqual(value, 15)

    def testValueOfTwentyReturnsTwenty(self):
        value = ultrak498.bcd_to_int(chr(0x02))
        self.assertEqual(value, 20)

    def testValueOf42Returns42(self):
        value = ultrak498.bcd_to_int(chr(0x24))
        self.assertEqual(value, 42)

    def testValueOf50Returns50(self):
        value = ultrak498.bcd_to_int(chr(0x05))
        self.assertEqual(value, 50)

    def testValueOf75Returns75(self):
        value = ultrak498.bcd_to_int(chr(0x57))
        self.assertEqual(value, 75)

    def testValueOf98Returns98(self):
        value = ultrak498.bcd_to_int(chr(0x89))
        self.assertEqual(value, 98)

    def testValueOf99Returns99(self):
        value = ultrak498.bcd_to_int(chr(0x99))
        self.assertEqual(value, 99)

    def testMultiByteStringRaisesException(self):
        with self.assertRaises(ValueError):
            ultrak498.bcd_to_int("ab")

    def testOnesPlaceGreaterThanNineRaisesException(self):
        with self.assertRaises(ValueError):
            ultrak498.bcd_to_int(chr(0xA0))

    def testTensPlaceGreaterThanNineRaisesException(self):
        with self.assertRaises(ValueError):
            ultrak498.bcd_to_int(chr(0x0A))

##############################################################################
# vim: ts=4 sts=4 sw=4 tw=78 sta et
##############################################################################
