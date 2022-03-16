import os
from conan import ConanFile
from conan.tools.apple import XcodeBuild
from conan.tools.files import copy

class HelloLib(ConanFile):
    name = "hello"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "XcodeToolchain"
    exports_sources = "HelloLibrary.xcodeproj/*", "src/*"

    def build(self):
        xcode = XcodeBuild(self)
        xcode.build("HelloLibrary.xcodeproj")

    def package(self):
        copy(self, "*/libhello.a", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "src/hello.hpp", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]