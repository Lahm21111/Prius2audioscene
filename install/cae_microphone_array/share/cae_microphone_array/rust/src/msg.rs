#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to cae_microphone_array__msg__AudioStream

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AudioStream {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


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
    pub data: Vec<u8>,

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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::AudioStream::default())
  }
}

impl rosidl_runtime_rs::Message for AudioStream {
  type RmwMsg = super::msg::rmw::AudioStream;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        encoding: msg.encoding,
        is_bigendian: msg.is_bigendian,
        channels: msg.channels,
        sample_rate: msg.sample_rate,
        data: msg.data.into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      encoding: msg.encoding,
      is_bigendian: msg.is_bigendian,
      channels: msg.channels,
      sample_rate: msg.sample_rate,
        data: msg.data.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      encoding: msg.encoding,
      is_bigendian: msg.is_bigendian,
      channels: msg.channels,
      sample_rate: msg.sample_rate,
      data: msg.data
          .into_iter()
          .collect(),
    }
  }
}


