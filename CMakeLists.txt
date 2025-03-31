
cmake_minimum_required(VERSION 3.13)

# Get these files from your pico-sdk installation
set(PICO_SDK_PATH ${CMAKE_SOURCE_DIR}/pico-sdk)
include(${CMAKE_SOURCE_DIR}/pico_sdk_import.cmake)
include(${CMAKE_SOURCE_DIR}/pico-lib/pico_lib_import.cmake)

project(pico_project)

pico_sdk_init()

add_executable(pico_project
    main.c
)

target_link_libraries(pico_project 
    pico_stdlib
    pico-lib
)

pico_add_extra_outputs(pico_project)
