#include "hello.hpp"
#include <iostream>

void hello(){
    #ifndef DEBUG
    std::cout << "App Release!" << std::endl;
    #else
    std::cout << "App Debug!" << std::endl;
    #endif
}
