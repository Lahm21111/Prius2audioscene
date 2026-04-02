// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from cae_microphone_array:msg/AudioStream.idl
// generated code does not contain a copyright notice

#ifndef CAE_MICROPHONE_ARRAY__MSG__DETAIL__AUDIO_STREAM__BUILDER_HPP_
#define CAE_MICROPHONE_ARRAY__MSG__DETAIL__AUDIO_STREAM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "cae_microphone_array/msg/detail/audio_stream__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace cae_microphone_array
{

namespace msg
{

namespace builder
{

class Init_AudioStream_data
{
public:
  explicit Init_AudioStream_data(::cae_microphone_array::msg::AudioStream & msg)
  : msg_(msg)
  {}
  ::cae_microphone_array::msg::AudioStream data(::cae_microphone_array::msg::AudioStream::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cae_microphone_array::msg::AudioStream msg_;
};

class Init_AudioStream_sample_rate
{
public:
  explicit Init_AudioStream_sample_rate(::cae_microphone_array::msg::AudioStream & msg)
  : msg_(msg)
  {}
  Init_AudioStream_data sample_rate(::cae_microphone_array::msg::AudioStream::_sample_rate_type arg)
  {
    msg_.sample_rate = std::move(arg);
    return Init_AudioStream_data(msg_);
  }

private:
  ::cae_microphone_array::msg::AudioStream msg_;
};

class Init_AudioStream_channels
{
public:
  explicit Init_AudioStream_channels(::cae_microphone_array::msg::AudioStream & msg)
  : msg_(msg)
  {}
  Init_AudioStream_sample_rate channels(::cae_microphone_array::msg::AudioStream::_channels_type arg)
  {
    msg_.channels = std::move(arg);
    return Init_AudioStream_sample_rate(msg_);
  }

private:
  ::cae_microphone_array::msg::AudioStream msg_;
};

class Init_AudioStream_is_bigendian
{
public:
  explicit Init_AudioStream_is_bigendian(::cae_microphone_array::msg::AudioStream & msg)
  : msg_(msg)
  {}
  Init_AudioStream_channels is_bigendian(::cae_microphone_array::msg::AudioStream::_is_bigendian_type arg)
  {
    msg_.is_bigendian = std::move(arg);
    return Init_AudioStream_channels(msg_);
  }

private:
  ::cae_microphone_array::msg::AudioStream msg_;
};

class Init_AudioStream_encoding
{
public:
  explicit Init_AudioStream_encoding(::cae_microphone_array::msg::AudioStream & msg)
  : msg_(msg)
  {}
  Init_AudioStream_is_bigendian encoding(::cae_microphone_array::msg::AudioStream::_encoding_type arg)
  {
    msg_.encoding = std::move(arg);
    return Init_AudioStream_is_bigendian(msg_);
  }

private:
  ::cae_microphone_array::msg::AudioStream msg_;
};

class Init_AudioStream_header
{
public:
  Init_AudioStream_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AudioStream_encoding header(::cae_microphone_array::msg::AudioStream::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_AudioStream_encoding(msg_);
  }

private:
  ::cae_microphone_array::msg::AudioStream msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::cae_microphone_array::msg::AudioStream>()
{
  return cae_microphone_array::msg::builder::Init_AudioStream_header();
}

}  // namespace cae_microphone_array

#endif  // CAE_MICROPHONE_ARRAY__MSG__DETAIL__AUDIO_STREAM__BUILDER_HPP_
