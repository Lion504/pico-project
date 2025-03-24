cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)
include(pico-lib/pico_lib_import.cmake)

project(my_pico_project C CXX ASM)
pico_sdk_init()

add_subdirectory(pico-lib)

add_executable(my_pico_project
    main.c
)

target_link_libraries(my_pico_project
    pico_stdlib
    pico-lib
    # Add any other libraries from pico-lib you need
)

pico_add_extra_outputs(my_pico_project)
