#!/bin/bash
set -e

BUILD_DIR=build
if [ -d "$BUILD_DIR" ]; then
    rm -rf "$BUILD_DIR"
fi

cmake -B build -S . -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
