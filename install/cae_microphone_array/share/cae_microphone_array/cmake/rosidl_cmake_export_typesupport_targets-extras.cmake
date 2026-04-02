# generated from
# rosidl_cmake/cmake/template/rosidl_cmake_export_typesupport_targets.cmake.in

set(_exported_typesupport_targets
  "__rosidl_generator_c:cae_microphone_array__rosidl_generator_c;__rosidl_typesupport_fastrtps_c:cae_microphone_array__rosidl_typesupport_fastrtps_c;__rosidl_typesupport_introspection_c:cae_microphone_array__rosidl_typesupport_introspection_c;__rosidl_typesupport_c:cae_microphone_array__rosidl_typesupport_c;__rosidl_generator_cpp:cae_microphone_array__rosidl_generator_cpp;__rosidl_typesupport_fastrtps_cpp:cae_microphone_array__rosidl_typesupport_fastrtps_cpp;__rosidl_typesupport_introspection_cpp:cae_microphone_array__rosidl_typesupport_introspection_cpp;__rosidl_typesupport_cpp:cae_microphone_array__rosidl_typesupport_cpp;__rosidl_generator_py:cae_microphone_array__rosidl_generator_py")

# populate cae_microphone_array_TARGETS_<suffix>
if(NOT _exported_typesupport_targets STREQUAL "")
  # loop over typesupport targets
  foreach(_tuple ${_exported_typesupport_targets})
    string(REPLACE ":" ";" _tuple "${_tuple}")
    list(GET _tuple 0 _suffix)
    list(GET _tuple 1 _target)

    set(_target "cae_microphone_array::${_target}")
    if(NOT TARGET "${_target}")
      # the exported target must exist
      message(WARNING "Package 'cae_microphone_array' exports the typesupport target '${_target}' which doesn't exist")
    else()
      list(APPEND cae_microphone_array_TARGETS${_suffix} "${_target}")
    endif()
  endforeach()
endif()
