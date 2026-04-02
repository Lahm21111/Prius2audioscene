#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "cae_microphone_array__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__cae_microphone_array__msg__AudioStream() -> *const std::ffi::c_void;
}

#[link(name = "cae_microphone_array__rosidl_generator_c")]
extern "C" {
    fn cae_microphone_array__msg__AudioStream__init(msg: *mut AudioStream) -> bool;
    fn cae_microphone_array__msg__AudioStream__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<AudioStream>, size: usize) -> bool;
    fn cae_microphone_array__msg__AudioStream__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<AudioStream>);
    fn cae_microphone_array__msg__AudioStream__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<AudioStream>, out_seq: *mut rosidl_runtime_rs::Sequence<AudioStream>) -> bool;
}

// Corresponds to cae_microphone_array__msg__AudioStream
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AudioStream {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub encoding: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub is_bigendian: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub channels: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sample_rate: u32,

    /// interleaved channels
    pub data: rosidl_runtime_rs::Sequence<u8>,

}

impl AudioStream {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const SINT_8_PCM: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const UINT_8_PCM: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const SINT_16_PCM: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const SINT_24_PCM: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const SINT_32_PCM: u8 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const FLOAT_32: u8 = 5;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const FLOAT_64: u8 = 6;

}


impl Default for AudioStream {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !cae_microphone_array__msg__AudioStream__init(&mut msg as *mut _) {
        panic!("Call to cae_microphone_array__msg__AudioStream__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for AudioStream {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { cae_microphone_array__msg__AudioStream__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { cae_microphone_array__msg__AudioStream__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { cae_microphone_array__msg__AudioStream__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for AudioStream {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for AudioStream where Self: Sized {
  const TYPE_NAME: &'static str = "cae_microphone_array/msg/AudioStream";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__cae_microphone_array__msg__AudioStream() }
  }
}


