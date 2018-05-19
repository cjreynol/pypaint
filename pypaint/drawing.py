from functools import total_ordering
from struct import pack, unpack

from pypaint.shape_type import ShapeType


@total_ordering
class Drawing:
    """
    """

    HEADER_SIZE = 8
    HEADER_VERSION = 1
    HEADER_PACK_STR = "II"

    MSG_SIZE = 28
    MSG_PACK_STR = "d5i"

    def __init__(self, timestamp, shape, coords):
        self.timestamp = timestamp
        self.shape = shape
        self.coords = coords

    def encode(self):
        """
        Return a byte array representing this instance.
        """
        drawing_bytes =  pack(self.MSG_PACK_STR, self.timestamp, 
                                self.shape.value, *self.coords)
        header = self.create_header(drawing_bytes)
        return header + drawing_bytes

    def create_header(self, bytes_msg):
        """
        Return a byte array representing a header for the given message.
        """
        non_header_length = len(bytes_msg)
        return pack(self.HEADER_PACK_STR, self.HEADER_VERSION, 
                        non_header_length)

    @staticmethod
    def decode_drawings(byte_array):
        """
        Return a list of the decoded drawings in the byte array.
        """
        drawings = []
        for i in range(len(byte_array) // Drawing.MSG_SIZE):
            msg_start = i * Drawing.MSG_SIZE
            msg_end = msg_start + Drawing.MSG_SIZE
            drawings.append(Drawing.decode_drawing(byte_array[msg_start:msg_end]))
        return drawings

    @staticmethod
    def decode_drawing(byte_array):
        """
        Return a Drawing instance using the data from the byte array.
        """
        drawing = None
        if len(byte_array) == Drawing.MSG_SIZE:
            timestamp, shape_val, *coords = unpack(Drawing.MSG_PACK_STR, 
                                                    byte_array)
            drawing = Drawing(timestamp, ShapeType(shape_val), coords)
        else:
            print(len(byte_array))
        return drawing

    @staticmethod
    def decode_header(byte_array):
        """
        Return the version number and message length from the byte_array.
        """
        return unpack(Drawing.HEADER_PACK_STR, byte_array)
        
    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __eq__(self, other):
        equal = False
        if isinstance(self, other.__class__):
            return (self.timestamp == other.timestamp
                        and self.shape == other.shape
                        and self.coords == other.coords)

    def hash(self):
        return hash((self.timestamp, self.shape, self.coords))
