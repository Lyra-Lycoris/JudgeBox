cmake_minimum_required(VERSION 3.20)

project(JudgeBox LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)#指定c++版本
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(
    JudgeBox src/main.cpp #主程序
    src/process_win32.cpp #启动外部程序，传递输入，收集输出和错误信息
    )

target_include_directories(JudgeBox PRIVATE # 头文件查找目录
    src
)

add_executable(ExitCode7
    tests/ExitCode7.cpp
)