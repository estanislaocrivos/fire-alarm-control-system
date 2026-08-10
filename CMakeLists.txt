cmake_minimum_required(VERSION 3.13)
project(my-app LANGUAGES C)

set(BOARD "" CACHE STRING "Target board (see external/c-libraries/boards/)")
set(MCU_FLAGS "" CACHE STRING "Compiler/linker flags for the target MCU (e.g. -mmcu=atmega2560)")
set(F_CPU "" CACHE STRING "CPU clock frequency in Hz")

if(NOT BOARD)
    message(FATAL_ERROR "BOARD is not defined. Must define it with -DBOARD=<name>")
endif()

if(MCU_FLAGS)
    separate_arguments(MCU_FLAGS_LIST UNIX_COMMAND "${MCU_FLAGS}")
    add_compile_options(${MCU_FLAGS_LIST})
    add_link_options(${MCU_FLAGS_LIST})
endif()

if(F_CPU)
    add_compile_definitions(F_CPU=${F_CPU})
endif()

add_subdirectory(external/c-libraries)

add_executable(my-app src/main.c)
target_link_libraries(my-app PRIVATE board)

if(CMAKE_OBJCOPY)
    add_custom_command(TARGET my-app POST_BUILD
        COMMAND ${CMAKE_OBJCOPY} -O ihex -R .eeprom $<TARGET_FILE:my-app> $<TARGET_FILE:my-app>.hex
        COMMENT "Generating Intel HEX image ($<TARGET_FILE:my-app>.hex)"
    )
endif()
