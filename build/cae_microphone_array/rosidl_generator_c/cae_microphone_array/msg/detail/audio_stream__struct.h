// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from cae_microphone_array:msg/AudioStream.idl
// generated code does not contain a copyright notice

#ifndef CAE_MICROPHONE_ARRAY__MSG__DETAIL__AUDIO_STREAM__STRUCT_H_
#define CAE_MICROPHONE_ARRAY__MSG__DETAIL__AUDIO_STREAM__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'SINT_8_PCM'.
enum
{
  cae_microphone_array__msg__AudioStream__SINT_8_PCM = 0
};

/// Constant 'UINT_8_PCM'.
enum
{
  cae_microphone_array__msg__AudioStream__UINT_8_PCM = 1
};

/// Constant 'SINT_16_PCM'.
enum
{
  cae_microphone_array__msg__AudioStream__SINT_16_PCM = 2
};

/// Constant 'SINT_24_PCM'.
enum
{
  cae_microphone_array__msg__AudioStream__SINT_24_PCM = 3
};

/// Constant 'SINT_32_PCM'.
enum
{
  cae_microphone_array__msg__AudioStream__SINT_32_PCM = 4
};

/// Constant 'FLOAT_32'.
enum
{
  cae_microphone_array__msg__AudioStream__FLOAT_32 = 5
};

/// Constant 'FLOAT_64'.
enum
{
  cae_microphone_array__msg__AudioStream__FLOAT_64 = 6
};

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'data'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/AudioStream in the package cae_microphone_array.
typedef struct cae_microphone_array__msg__AudioStream
{
  std_msgs__msg__Header header;
  uint8_t encoding;
  uint8_t is_bigendian;
  uint8_t channels;
  uint32_t sample_rate;
  /// interleaved channels
  rosidl_runtime_c__uint8__Sequence data;
} cae_microphone_array__msg__AudioStream;

// Struct for a sequence of cae_microphone_array__msg__AudioStream.
typedef struct cae_microphone_array__msg__AudioStream__Sequence
{
  cae_microphone_array__msg__AudioStream * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cae_microphone_array__msg__AudioStream__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CAE_MICROPHONE_ARRAY__MSG__DETAIL__AUDIO_STREAM__STRUCT_H_
