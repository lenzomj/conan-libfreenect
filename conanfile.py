from conans import ConanFile, CMake, tools


class LibfreenectConan(ConanFile):
    name = "libfreenect"
    version = "0.6.2"
    license = "MIT"
    author = "Matthew J. Lenzo"
    url = "https://github.com/lenzomj/conan-libfreenect"
    description = "libfreenect is a userspace driver for the Microsoft Kinect"
    topics = ("kinect", "opencv", "driver")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"

    build_dir = "build"
    install_dir = "install"

    #def config_options(self):
    #    if self.settings.os == "Windows":
    #        del self.options.fPIC

    def source(self):
        self.run("git clone https://github.com/OpenKinect/libfreenect.git --branch %s" % self.version)
        tools.replace_in_file("CMakeLists.txt",
                              "PROJECT(libfreenect)",
                              '''
                              PROJECT(libfreenect)
                              include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
                              conan_basic_setup()
                              ''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions['BUILD_AS3_SERVER'] = False
        cmake.definitions['BUILD_CPACK_DEB'] = False
        cmake.definitions['BUILD_CPACK_RPM'] = False
        cmake.definitions['BUILD_CPACK_TGZ'] = False
        cmake.definitions['BUILD_CPP'] = True
        cmake.definitions['BUILD_CV'] = False
        cmake.definitions['BUILD_C_SYNC'] = False
        cmake.definitions['BUILD_EXAMPLES'] = False
        cmake.definitions['BUILD_FAKENECT'] = False
        cmake.definitions['BUILD_OPENNI2_DRIVER'] = False
        cmake.definitions['BUILD_PYTHON'] = False
        cmake.definitions['BUILD_PYTHON2'] = False
        cmake.definitions['BUILD_PYTHON3'] = False
        cmake.definitions['BUILD_REDIST_PACKAGE'] = True

        tools.mkdir(self.build_dir)
        with tools.chdir(self.build_dir):
            cmake.configure(source_dir='..', build_dir='.')
            cmake.build()

    def package(self):
        self.copy('*.h', src='%s/include' % self.install_dir, dst='include')
        self.copy('libfreenect.so', src='%s/lib' % self.install_dir, dst='lib')

    def package_info(self):
        self.cpp_info.libs = ["libfreenect"]

