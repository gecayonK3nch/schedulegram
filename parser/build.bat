@echo off
chcp 65001

set BUILD_DIR = build
if exist %BUILD_DIR% rmdir /s /q %BUILD_DIR%

cmake -B build -S . -G "Visual Studio 17 2022"
cmake --build build
