// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from cae_microphone_array:msg/AudioStream.idl
// generated code does not contain a copyright notice

#ifndef CAE_MICROPHONE_ARRAY__MSG__DETAIL__AUDIO_STREAM__STRUCT_HPP_
#define CAE_MICROPHONE_ARRAY__MSG__DETAIL__AUDIO_STREAM__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__cae_microphone_array__msg__AudioStream __attribute__((deprecated))
#else
# define DEPRECATED__cae_microphone_array__msg__AudioStream __declspec(deprecated)
#endif

namespace cae_microphone_array
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct AudioStream_
{
  using Type = AudioStream_<ContainerAllocator>;

  explicit AudioStream_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->encoding = 0;
      this->is_bigendian = 0;
      this->channels = 0;
      this->sample_rate = 0ul;
    }
  }

  explicit AudioStream_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->encoding = 0;
      this->is_bigendian = 0;
      this->channels = 0;
      this->sample_rate = 0ul;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _encoding_type =
    uint8_t;
  _encoding_type encoding;
  using _is_bigendian_type =
    uint8_t;
  _is_bigendian_type is_bigendian;
  using _channels_type =
    uint8_t;
  _channels_type channels;
  using _sample_rate_type =
    uint32_t;
  _sample_rate_type sample_rate;
  using _data_type =
    std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>>;
  _data_type data;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__encoding(
    const uint8_t & _arg)
  {
    this->encoding = _arg;
    return *this;
  }
  Type & set__is_bigendian(
    const uint8_t & _arg)
  {
    this->is_bigendian = _arg;
    return *this;
  }
  Type & set__channels(
    const uint8_t & _arg)
  {
    this->channels = _arg;
    return *this;
  }
  Type & set__sample_rate(
    const uint32_t & _arg)
  {
    this->sample_rate = _arg;
    return *this;
  }
  Type & set__data(
    const std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>> & _arg)
  {
    this->data = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t SINT_8_PCM =
    0u;
  static constexpr uint8_t UINT_8_PCM =
    1u;
  static constexpr uint8_t SINT_16_PCM =
    2u;
  static constexpr uint8_t SINT_24_PCM =
    3u;
  static constexpr uint8_t SINT_32_PCM =
    4u;
  static constexpr uint8_t FLOAT_32 =
    5u;
  static constexpr uint8_t FLOAT_64 =
    6u;

  // pointer types
  using RawPtr =
    cae_microphone_array::msg::AudioStream_<ContainerAllocator> *;
  using ConstRawPtr =
    const cae_microphone_array::msg::AudioStream_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cae_microphone_array::msg::AudioStream_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cae_microphone_array::msg::AudioStream_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cae_microphone_array::msg::AudioStream_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cae_microphone_array::msg::AudioStream_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cae_microphone_array::msg::AudioStream_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cae_microphone_array::msg::AudioStream_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cae_microphone_array::msg::AudioStream_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cae_microphone_array::msg::AudioStream_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cae_microphone_array__msg__AudioStream
    std::shared_ptr<cae_microphone_array::msg::AudioStream_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cae_microphone_array__msg__AudioStream
    std::shared_ptr<cae_microphone_array::msg::AudioStream_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const AudioStream_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->encoding != other.encoding) {
      return false;
    }
    if (this->is_bigendian != other.is_bigendian) {
      return false;
    }
    if (this->channels != other.channels) {
      return false;
    }
    if (this->sample_rate != other.sample_rate) {
      return false;
    }
    if (this->data != other.data) {
      return false;
    }
    return true;
  }
  bool operator!=(const AudioStream_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct AudioStream_

// alias to use template instance with default allocator
using AudioStream =
  cae_microphone_array::msg::AudioStream_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t AudioStream_<ContainerAllocator>::SINT_8_PCM;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t AudioStream_<ContainerAllocator>::UINT_8_PCM;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t AudioStream_<ContainerAllocator>::SINT_16_PCM;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t AudioStream_<ContainerAllocator>::SINT_24_PCM;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t AudioStream_<ContainerAllocator>::SINT_32_PCM;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t AudioStream_<ContainerAllocator>::FLOAT_32;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t AudioStream_<ContainerAllocator>::FLOAT_64;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace cae_microphone_array

#endif  // CAE_MICROPHONE_ARRAY__MSG__DETAIL__AUDIO_STREAM__STRUCT_HPP_
