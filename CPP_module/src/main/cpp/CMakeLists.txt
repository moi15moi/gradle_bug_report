cmake_minimum_required(VERSION 3.22.1)

project("CPP_module")

add_library(${CMAKE_PROJECT_NAME} SHARED
    c_file.c)

target_include_directories(${CMAKE_PROJECT_NAME} PUBLIC include)

target_link_libraries(${CMAKE_PROJECT_NAME}
    android
    log)
 