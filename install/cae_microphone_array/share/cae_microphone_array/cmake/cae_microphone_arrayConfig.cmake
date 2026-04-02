# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_cae_microphone_array_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED cae_microphone_array_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(cae_microphone_array_FOUND FALSE)
  elseif(NOT cae_microphone_array_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(cae_microphone_array_FOUND FALSE)
  endif()
  return()
endif()
set(_cae_microphone_array_CONFIG_INCLUDED TRUE)

# output package information
if(NOT cae_microphone_array_FIND_QUIETLY)
  message(STATUS "Found cae_microphone_array: 0.0.1 (${cae_microphone_array_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'cae_microphone_array' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${cae_microphone_array_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(cae_microphone_array_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "rosidl_cmake-extras.cmake;ament_cmake_export_dependencies-extras.cmake;ament_cmake_export_include_directories-extras.cmake;ament_cmake_export_libraries-extras.cmake;ament_cmake_export_targets-extras.cmake;rosidl_cmake_export_typesupport_targets-extras.cmake;rosidl_cmake_export_typesupport_libraries-extras.cmake")
foreach(_extra ${_extras})
  include("${cae_microphone_array_DIR}/${_extra}")
endforeach()
