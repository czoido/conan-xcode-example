import os
from conan import ConanFile
from conan.tools.apple import XcodeBuild
from conan.tools.files import copy
from conan.tools.scm import Git
from conan.tools.files import load, update_conandata


class HelloLib(ConanFile):
    name = "hello"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "XcodeToolchain"
    exports_sources = "HelloLibrary.xcodeproj/*", "src/*"

    def export(self):
        git = Git(self, self.recipe_folder)
        scm_url, scm_commit = git.get_url_and_commit()
        # we store the current url and commit in conandata.yml
        update_conandata(self, {"sources": {"commit": scm_commit, "url": scm_url}})

    def build(self):
        xcode = XcodeBuild(self)
        xcode.build("HelloLibrary.xcodeproj")

    def package(self):
        copy(self, "*/libhello.a", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "src/hello.hpp", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]