// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from cae_microphone_array:msg/AudioStream.idl
// generated code does not contain a copyright notice

#ifndef CAE_MICROPHONE_ARRAY__MSG__DETAIL__AUDIO_STREAM__TRAITS_HPP_
#define CAE_MICROPHONE_ARRAY__MSG__DETAIL__AUDIO_STREAM__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "cae_microphone_array/msg/detail/audio_stream__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace cae_microphone_array
{

namespace msg
{

inline void to_flow_style_yaml(
  const AudioStream & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: encoding
  {
    out << "encoding: ";
    rosidl_generator_traits::value_to_yaml(msg.encoding, out);
    out << ", ";
  }

  // member: is_bigendian
  {
    out << "is_bigendian: ";
    rosidl_generator_traits::value_to_yaml(msg.is_bigendian, out);
    out << ", ";
  }

  // member: channels
  {
    out << "channels: ";
    rosidl_generator_traits::value_to_yaml(msg.channels, out);
    out << ", ";
  }

  // member: sample_rate
  {
    out << "sample_rate: ";
    rosidl_generator_traits::value_to_yaml(msg.sample_rate, out);
    out << ", ";
  }

  // member: data
  {
    if (msg.data.size() == 0) {
      out << "data: []";
    } else {
      out << "data: [";
      size_t pending_items = msg.data.size();
      for (auto item : msg.data) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const AudioStream & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: encoding
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "encoding: ";
    rosidl_generator_traits::value_to_yaml(msg.encoding, out);
    out << "\n";
  }

  // member: is_bigendian
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_bigendian: ";
    rosidl_generator_traits::value_to_yaml(msg.is_bigendian, out);
    out << "\n";
  }

  // member: channels
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "channels: ";
    rosidl_generator_traits::value_to_yaml(msg.channels, out);
    out << "\n";
  }

  // member: sample_rate
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sample_rate: ";
    rosidl_generator_traits::value_to_yaml(msg.sample_rate, out);
    out << "\n";
  }

  // member: data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.data.size() == 0) {
      out << "data: []\n";
    } else {
      out << "data:\n";
      for (auto item : msg.data) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const AudioStream & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace cae_microphone_array

namespace rosidl_generator_traits
{

[[deprecated("use cae_microphone_array::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const cae_microphone_array::msg::AudioStream & msg,
  std::ostream & out, size_t indentation = 0)
{
  cae_microphone_array::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use cae_microphone_array::msg::to_yaml() instead")]]
inline std::string to_yaml(const cae_microphone_array::msg::AudioStream & msg)
{
  return cae_microphone_array::msg::to_yaml(msg);
}

template<>
inline const char * data_type<cae_microphone_array::msg::AudioStream>()
{
  return "cae_microphone_array::msg::AudioStream";
}

template<>
inline const char * name<cae_microphone_array::msg::AudioStream>()
{
  return "cae_microphone_array/msg/AudioStream";
}

template<>
struct has_fixed_size<cae_microphone_array::msg::AudioStream>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<cae_microphone_array::msg::AudioStream>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<cae_microphone_array::msg::AudioStream>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CAE_MICROPHONE_ARRAY__MSG__DETAIL__AUDIO_STREAM__TRAITS_HPP_
