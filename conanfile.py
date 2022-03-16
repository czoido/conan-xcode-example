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

    def layout(self):
        print("------>>>", self.folders.source)

    def export(self):
        git = Git(self, self.recipe_folder)
        scm_url, scm_commit = git.get_url_and_commit()
        # we store the current url and commit in conandata.yml
        print(scm_url)
        print(scm_commit)
        update_conandata(self, {"sources": {"commit": scm_commit, "url": scm_url}})

    def source(self):
        # we recover the saved url and commit from conandata.yml and use them to get sources
        git = Git(self)
        sources = self.conan_data["sources"]
        git.clone(url=sources["url"], target=".")
        git.checkout(commit=sources["commit"])

    def build(self):
        xcode = XcodeBuild(self)
        xcode.build("HelloLibrary.xcodeproj")

    def package(self):
        copy(self, "*/libhello.a", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, "src/hello.hpp", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]