#!/bin/bash

cmake -S . -B build \
    -DCMAKE_TOOLCHAIN_FILE=external/c-libraries/cmake/toolchains/avr.cmake \
    -DBOARD=arduino_mega_2560 \
    -DMCU_FLAGS="-mmcu=atmega2560" \
    -DF_CPU=16000000UL \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

cmake --build build
