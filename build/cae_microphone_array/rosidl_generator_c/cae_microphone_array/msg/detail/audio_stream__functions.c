// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from cae_microphone_array:msg/AudioStream.idl
// generated code does not contain a copyright notice
#include "cae_microphone_array/msg/detail/audio_stream__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
cae_microphone_array__msg__AudioStream__init(cae_microphone_array__msg__AudioStream * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    cae_microphone_array__msg__AudioStream__fini(msg);
    return false;
  }
  // encoding
  // is_bigendian
  // channels
  // sample_rate
  // data
  if (!rosidl_runtime_c__uint8__Sequence__init(&msg->data, 0)) {
    cae_microphone_array__msg__AudioStream__fini(msg);
    return false;
  }
  return true;
}

void
cae_microphone_array__msg__AudioStream__fini(cae_microphone_array__msg__AudioStream * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // encoding
  // is_bigendian
  // channels
  // sample_rate
  // data
  rosidl_runtime_c__uint8__Sequence__fini(&msg->data);
}

bool
cae_microphone_array__msg__AudioStream__are_equal(const cae_microphone_array__msg__AudioStream * lhs, const cae_microphone_array__msg__AudioStream * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // encoding
  if (lhs->encoding != rhs->encoding) {
    return false;
  }
  // is_bigendian
  if (lhs->is_bigendian != rhs->is_bigendian) {
    return false;
  }
  // channels
  if (lhs->channels != rhs->channels) {
    return false;
  }
  // sample_rate
  if (lhs->sample_rate != rhs->sample_rate) {
    return false;
  }
  // data
  if (!rosidl_runtime_c__uint8__Sequence__are_equal(
      &(lhs->data), &(rhs->data)))
  {
    return false;
  }
  return true;
}

bool
cae_microphone_array__msg__AudioStream__copy(
  const cae_microphone_array__msg__AudioStream * input,
  cae_microphone_array__msg__AudioStream * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // encoding
  output->encoding = input->encoding;
  // is_bigendian
  output->is_bigendian = input->is_bigendian;
  // channels
  output->channels = input->channels;
  // sample_rate
  output->sample_rate = input->sample_rate;
  // data
  if (!rosidl_runtime_c__uint8__Sequence__copy(
      &(input->data), &(output->data)))
  {
    return false;
  }
  return true;
}

cae_microphone_array__msg__AudioStream *
cae_microphone_array__msg__AudioStream__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cae_microphone_array__msg__AudioStream * msg = (cae_microphone_array__msg__AudioStream *)allocator.allocate(sizeof(cae_microphone_array__msg__AudioStream), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(cae_microphone_array__msg__AudioStream));
  bool success = cae_microphone_array__msg__AudioStream__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
cae_microphone_array__msg__AudioStream__destroy(cae_microphone_array__msg__AudioStream * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    cae_microphone_array__msg__AudioStream__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
cae_microphone_array__msg__AudioStream__Sequence__init(cae_microphone_array__msg__AudioStream__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cae_microphone_array__msg__AudioStream * data = NULL;

  if (size) {
    data = (cae_microphone_array__msg__AudioStream *)allocator.zero_allocate(size, sizeof(cae_microphone_array__msg__AudioStream), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = cae_microphone_array__msg__AudioStream__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        cae_microphone_array__msg__AudioStream__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
cae_microphone_array__msg__AudioStream__Sequence__fini(cae_microphone_array__msg__AudioStream__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      cae_microphone_array__msg__AudioStream__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

cae_microphone_array__msg__AudioStream__Sequence *
cae_microphone_array__msg__AudioStream__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cae_microphone_array__msg__AudioStream__Sequence * array = (cae_microphone_array__msg__AudioStream__Sequence *)allocator.allocate(sizeof(cae_microphone_array__msg__AudioStream__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = cae_microphone_array__msg__AudioStream__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
cae_microphone_array__msg__AudioStream__Sequence__destroy(cae_microphone_array__msg__AudioStream__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    cae_microphone_array__msg__AudioStream__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
cae_microphone_array__msg__AudioStream__Sequence__are_equal(const cae_microphone_array__msg__AudioStream__Sequence * lhs, const cae_microphone_array__msg__AudioStream__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!cae_microphone_array__msg__AudioStream__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
cae_microphone_array__msg__AudioStream__Sequence__copy(
  const cae_microphone_array__msg__AudioStream__Sequence * input,
  cae_microphone_array__msg__AudioStream__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(cae_microphone_array__msg__AudioStream);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    cae_microphone_array__msg__AudioStream * data =
      (cae_microphone_array__msg__AudioStream *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!cae_microphone_array__msg__AudioStream__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          cae_microphone_array__msg__AudioStream__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!cae_microphone_array__msg__AudioStream__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
