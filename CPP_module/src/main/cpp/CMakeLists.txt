cmake_minimum_required(VERSION 3.22.1)
project("CPP_module")

add_library(${CMAKE_PROJECT_NAME} SHARED IMPORTED)
set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES
    IMPORTED_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/../jniLibs/${ANDROID_ABI}/libCPP_module.so)
