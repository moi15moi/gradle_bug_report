 cmake_minimum_required(VERSION 3.22.1)
 project("CPP_module")

 set(SO_FILE ${CMAKE_CURRENT_SOURCE_DIR}/../jniLibs/${ANDROID_ABI}/libCPP_module.so)

 add_library(${CMAKE_PROJECT_NAME} SHARED stub.c)

 set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES
         OUTPUT_NAME ${CMAKE_PROJECT_NAME}
         LIBRARY_OUTPUT_DIRECTORY ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})

 add_custom_command(TARGET ${CMAKE_PROJECT_NAME} POST_BUILD
         COMMAND ${CMAKE_COMMAND} -E copy_if_different ${SO_FILE} $<TARGET_FILE:${CMAKE_PROJECT_NAME}>
         COMMENT "Replacing with prebuilt libCPP_module.so")
