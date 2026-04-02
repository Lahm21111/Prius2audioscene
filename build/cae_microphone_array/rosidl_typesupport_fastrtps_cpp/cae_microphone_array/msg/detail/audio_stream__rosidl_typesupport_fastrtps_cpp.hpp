// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from cae_microphone_array:msg/AudioStream.idl
// generated code does not contain a copyright notice

#ifndef CAE_MICROPHONE_ARRAY__MSG__DETAIL__AUDIO_STREAM__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define CAE_MICROPHONE_ARRAY__MSG__DETAIL__AUDIO_STREAM__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "cae_microphone_array/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "cae_microphone_array/msg/detail/audio_stream__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace cae_microphone_array
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_cae_microphone_array
cdr_serialize(
  const cae_microphone_array::msg::AudioStream & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_cae_microphone_array
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  cae_microphone_array::msg::AudioStream & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_cae_microphone_array
get_serialized_size(
  const cae_microphone_array::msg::AudioStream & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_cae_microphone_array
max_serialized_size_AudioStream(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace cae_microphone_array

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_cae_microphone_array
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, cae_microphone_array, msg, AudioStream)();

#ifdef __cplusplus
}
#endif

#endif  // CAE_MICROPHONE_ARRAY__MSG__DETAIL__AUDIO_STREAM__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
