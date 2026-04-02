// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from cae_microphone_array:msg/AudioStream.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "cae_microphone_array/msg/detail/audio_stream__rosidl_typesupport_introspection_c.h"
#include "cae_microphone_array/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "cae_microphone_array/msg/detail/audio_stream__functions.h"
#include "cae_microphone_array/msg/detail/audio_stream__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__AudioStream_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  cae_microphone_array__msg__AudioStream__init(message_memory);
}

void cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__AudioStream_fini_function(void * message_memory)
{
  cae_microphone_array__msg__AudioStream__fini(message_memory);
}

size_t cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__size_function__AudioStream__data(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return member->size;
}

const void * cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__get_const_function__AudioStream__data(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void * cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__get_function__AudioStream__data(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__fetch_function__AudioStream__data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__get_const_function__AudioStream__data(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__assign_function__AudioStream__data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__get_function__AudioStream__data(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

bool cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__resize_function__AudioStream__data(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  rosidl_runtime_c__uint8__Sequence__fini(member);
  return rosidl_runtime_c__uint8__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__AudioStream_message_member_array[6] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cae_microphone_array__msg__AudioStream, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "encoding",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cae_microphone_array__msg__AudioStream, encoding),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "is_bigendian",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cae_microphone_array__msg__AudioStream, is_bigendian),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "channels",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cae_microphone_array__msg__AudioStream, channels),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "sample_rate",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cae_microphone_array__msg__AudioStream, sample_rate),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cae_microphone_array__msg__AudioStream, data),  // bytes offset in struct
    NULL,  // default value
    cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__size_function__AudioStream__data,  // size() function pointer
    cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__get_const_function__AudioStream__data,  // get_const(index) function pointer
    cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__get_function__AudioStream__data,  // get(index) function pointer
    cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__fetch_function__AudioStream__data,  // fetch(index, &value) function pointer
    cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__assign_function__AudioStream__data,  // assign(index, value) function pointer
    cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__resize_function__AudioStream__data  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__AudioStream_message_members = {
  "cae_microphone_array__msg",  // message namespace
  "AudioStream",  // message name
  6,  // number of fields
  sizeof(cae_microphone_array__msg__AudioStream),
  cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__AudioStream_message_member_array,  // message members
  cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__AudioStream_init_function,  // function to initialize message memory (memory has to be allocated)
  cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__AudioStream_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__AudioStream_message_type_support_handle = {
  0,
  &cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__AudioStream_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_cae_microphone_array
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, cae_microphone_array, msg, AudioStream)() {
  cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__AudioStream_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__AudioStream_message_type_support_handle.typesupport_identifier) {
    cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__AudioStream_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &cae_microphone_array__msg__AudioStream__rosidl_typesupport_introspection_c__AudioStream_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
