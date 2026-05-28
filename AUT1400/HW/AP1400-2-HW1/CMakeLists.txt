cmake_minimum_required(VERSION 3.14)
project(AP)

set(CMAKE_CXX_STANDARD 14)

include(FetchContent)
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG        v1.14.0
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

include_directories(include/)

add_executable(main
        src/main.cpp
        src/hw1.cpp
        src/unit_test.cpp
)
target_link_libraries(main
        gtest
        gtest_main
        gmock
)

