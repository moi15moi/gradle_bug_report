cmake_minimum_required(VERSION 3.22.1)

project("myapplication")

add_library(${CMAKE_PROJECT_NAME} SHARED
    # List C/C++ source files with relative paths to this CMakeLists.txt.
    native-lib.cpp)

find_package(CPP_module REQUIRED CONFIG)

target_link_libraries(${CMAKE_PROJECT_NAME}
    CPP_module::CPP_module
    android
    log)