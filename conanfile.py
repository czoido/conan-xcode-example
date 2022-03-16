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
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def build(self):
        xcode = XcodeBuild(self)
        xcode.build("HelloLibrary.xcodeproj")

    def package(self):
        copy(self, "*/libHelloLibrary*", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]