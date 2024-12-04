cmake_minimum_required(VERSION 3.15)
project(parser)

set(CMAKE_CXX_STANDARD 17)

set(CMAKE_TOOLCHAIN_FILE "C:/Users/gecay/OneDrive/Desktop/Projects/Bots/schedulegram/parser/vcpkg/scripts/buildsystems/vcpkg.cmake" CACHE STRING "Vcpkg toolchain file")
set(CMAKE_PREFIX_PATH "C:/Users/gecay/OneDrive/Desktop/Projects/Bots/schedulegram/parser/vcpkg/installed/x64-windows")

add_executable(parser main.cpp requests.cpp db_usage.cpp)

find_package(cpr CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)
find_package(unofficial-sqlite3 CONFIG REQUIRED)

target_link_libraries(parser PRIVATE cpr::cpr nlohmann_json::nlohmann_json unofficial::sqlite3::sqlite3)
