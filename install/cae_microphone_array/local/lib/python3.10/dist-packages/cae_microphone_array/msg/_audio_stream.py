# generated from rosidl_generator_py/resource/_idl.py.em
# with input from cae_microphone_array:msg/AudioStream.idl
# generated code does not contain a copyright notice


# Import statements for member types

# Member 'data'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_AudioStream(type):
    """Metaclass of message 'AudioStream'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'SINT_8_PCM': 0,
        'UINT_8_PCM': 1,
        'SINT_16_PCM': 2,
        'SINT_24_PCM': 3,
        'SINT_32_PCM': 4,
        'FLOAT_32': 5,
        'FLOAT_64': 6,
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('cae_microphone_array')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'cae_microphone_array.msg.AudioStream')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__audio_stream
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__audio_stream
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__audio_stream
            cls._TYPE_SUPPORT = module.type_support_msg__msg__audio_stream
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__audio_stream

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'SINT_8_PCM': cls.__constants['SINT_8_PCM'],
            'UINT_8_PCM': cls.__constants['UINT_8_PCM'],
            'SINT_16_PCM': cls.__constants['SINT_16_PCM'],
            'SINT_24_PCM': cls.__constants['SINT_24_PCM'],
            'SINT_32_PCM': cls.__constants['SINT_32_PCM'],
            'FLOAT_32': cls.__constants['FLOAT_32'],
            'FLOAT_64': cls.__constants['FLOAT_64'],
        }

    @property
    def SINT_8_PCM(self):
        """Message constant 'SINT_8_PCM'."""
        return Metaclass_AudioStream.__constants['SINT_8_PCM']

    @property
    def UINT_8_PCM(self):
        """Message constant 'UINT_8_PCM'."""
        return Metaclass_AudioStream.__constants['UINT_8_PCM']

    @property
    def SINT_16_PCM(self):
        """Message constant 'SINT_16_PCM'."""
        return Metaclass_AudioStream.__constants['SINT_16_PCM']

    @property
    def SINT_24_PCM(self):
        """Message constant 'SINT_24_PCM'."""
        return Metaclass_AudioStream.__constants['SINT_24_PCM']

    @property
    def SINT_32_PCM(self):
        """Message constant 'SINT_32_PCM'."""
        return Metaclass_AudioStream.__constants['SINT_32_PCM']

    @property
    def FLOAT_32(self):
        """Message constant 'FLOAT_32'."""
        return Metaclass_AudioStream.__constants['FLOAT_32']

    @property
    def FLOAT_64(self):
        """Message constant 'FLOAT_64'."""
        return Metaclass_AudioStream.__constants['FLOAT_64']


class AudioStream(metaclass=Metaclass_AudioStream):
    """
    Message class 'AudioStream'.

    Constants:
      SINT_8_PCM
      UINT_8_PCM
      SINT_16_PCM
      SINT_24_PCM
      SINT_32_PCM
      FLOAT_32
      FLOAT_64
    """

    __slots__ = [
        '_header',
        '_encoding',
        '_is_bigendian',
        '_channels',
        '_sample_rate',
        '_data',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'encoding': 'uint8',
        'is_bigendian': 'uint8',
        'channels': 'uint8',
        'sample_rate': 'uint32',
        'data': 'sequence<uint8>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('uint8')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.encoding = kwargs.get('encoding', int())
        self.is_bigendian = kwargs.get('is_bigendian', int())
        self.channels = kwargs.get('channels', int())
        self.sample_rate = kwargs.get('sample_rate', int())
        self.data = array.array('B', kwargs.get('data', []))

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.header != other.header:
            return False
        if self.encoding != other.encoding:
            return False
        if self.is_bigendian != other.is_bigendian:
            return False
        if self.channels != other.channels:
            return False
        if self.sample_rate != other.sample_rate:
            return False
        if self.data != other.data:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def encoding(self):
        """Message field 'encoding'."""
        return self._encoding

    @encoding.setter
    def encoding(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'encoding' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'encoding' field must be an unsigned integer in [0, 255]"
        self._encoding = value

    @builtins.property
    def is_bigendian(self):
        """Message field 'is_bigendian'."""
        return self._is_bigendian

    @is_bigendian.setter
    def is_bigendian(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'is_bigendian' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'is_bigendian' field must be an unsigned integer in [0, 255]"
        self._is_bigendian = value

    @builtins.property
    def channels(self):
        """Message field 'channels'."""
        return self._channels

    @channels.setter
    def channels(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'channels' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'channels' field must be an unsigned integer in [0, 255]"
        self._channels = value

    @builtins.property
    def sample_rate(self):
        """Message field 'sample_rate'."""
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'sample_rate' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'sample_rate' field must be an unsigned integer in [0, 4294967295]"
        self._sample_rate = value

    @builtins.property
    def data(self):
        """Message field 'data'."""
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'B', \
                "The 'data' array.array() must have the type code of 'B'"
            self._data = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, int) for v in value) and
                 all(val >= 0 and val < 256 for val in value)), \
                "The 'data' field must be a set or sequence and each value of type 'int' and each unsigned integer in [0, 255]"
        self._data = array.array('B', value)
