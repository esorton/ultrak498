##############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) 2014-2015 Eric F Sorton
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

from collections import namedtuple
import optparse
import sys
import serial

def bcd_to_int(bcd_byte):
    """Converts a packed, little-endian, binary coded decimal to an int.

    NOTE: byte must be a string (length of 1).  A ValueException is generated
    if the length is greater than 1 or if the decoded value is less than 0 or
    greater than 99.

    Returns a decimal value between 0 and 99.
    """

    # Method only works on single bytes.
    if len(bcd_byte) > 1:
        raise ValueError("Invalid length; bcdToInt() assumes single byte input.")

    # Get the tens place; value must be a single digit.
    tens = int((ord(bcd_byte) >> 0) & 0x0F)
    if (tens < 0) or (tens > 9):
        raise ValueError("Invalid BCD digit; tens place is not 0-9.")

    # Get the ones place; value must be a single digit.
    ones = int((ord(bcd_byte) >> 4) & 0x0F)
    if (ones < 0) or (ones > 9):
        raise ValueError("Invalid BCD digit; ones place is not 0-9.")

    return (tens*10 + ones)

def readRecord(in_file):
    """Generator to read each record from the input file.

    Returns the next record as a named tuples.
    """

    # Dictionary mapping type id to record named tuples.
    recordTypes = {
         0: namedtuple("RaceHeaderRecord", "type year month day id"),
        10: namedtuple("LapTimeRecord",    "type minutes seconds hundreths lap"),
        20: namedtuple("AbsTimeRecord",    "type minutes seconds hundreths lap"),
        30: namedtuple("Type30Record",     "type a b c laps"),
        40: namedtuple("Type40Record",     "type a b c laps"),
        50: namedtuple("RaceEndRecord",    "type minutes seconds hundreths laps"),
        }

    # Need to track hundreds place manually since single byte BCD can't
    # represent a number greater than 100.
    lap_hundreds = 0
    abs_hundreds = 0

    # Loop till end-of-file or timeout (in the case of a serial connection).
    while True:

        # Records are always five bytes wide; read one record.
        record_bytes = in_file.read(5)
        if not record_bytes:
            break
        if len(record_bytes) != 5:
            raise ValueError(":TODO:")

        # Convert raw BCD bytes to integers.
        record_bytes = [bcdTOint(byte) for byte in record_bytes]

        # First byte is the record type; record type must be known.
        record_type = record_bytes[0]
        if record_type not in recordTypes:
            raise ValueError(":TODO:")

        # Create a namedtuple based upon the record_type.
        record = recordTypes[record_type]._make(record_bytes)

        # Adjust the hundreds of the lap/place record if needed.
        if (record.type == 10) and (record.lap == 0):
            lap_hundreds += 100
            record = record._replace(lap=(record.lap + lap_hundreds))
        if (record.type == 20) and (record.lap == 0):
            abs_hundreds += 100
            record = record._replace(lap=(record.lap + abs_hundreds))

        yield record

def openFile(infile):
    """Attempts to open the given file.

    Returns a file object.
    """

    # First, check if in_file is a file object.
    if isinstance(infile, file):
        return infile

    # Next, check if it is a serial port we can open.  Ignore exceptions so we
    # can try to open infile as a normal file next.
    try:
        return serial.Serial(infile, baudrate=4800, timeout=10)
    except:
        pass

    # Finally, try to open it as a normal file.  Let open() throw its
    # exception normally on failure.
    return open(infile, "rb")


def readRecords(infile):
    """Reads all records from the input file.

    Returns a list of named tuples, one for each record read.
    """
    infile = openFile(infile)
    return [record for record in readRecord(infile)]

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", "--infile",   dest="infile",   metavar="FILE",           default=sys.stdin,  help="Input file, stdin if not specified.")
    parser.add_option("-o", "--outfile",  dest="outfile",  metavar="FILE",           default=sys.stdout, help="Output file, stdout if not specified.")
    parser.add_option("-r", "--raceid",   dest="raceid",   metavar="NUM",  type=int, default=1,          help="Race ID to display.")
    (options, args) = parser.parse_args()

    current_race = 0
    for record in readRecords(options.infile):
        if record.type == 0:
            current_race = record.id
        if (record.type == 20) and (current_race == options.raceid):
            total_in_hundreths = record.minutes*60*100 + record.seconds*100 + record.hundreths
            print "{},{}:{:02}.{:02},{}".format(record.lap,record.minutes,record.seconds,record.hundreths,total_in_hundreths)

##############################################################################
# vim: ts=4 sts=4 sw=4 tw=78 sta et
##############################################################################
