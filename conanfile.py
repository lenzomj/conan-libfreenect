from conans import ConanFile, CMake, tools


class LibfreenectConan(ConanFile):
    name = "libfreenect"
    version = "v0.6.2"
    license = "MIT"
    author = "Matthew J. Lenzo"
    url = "https://github.com/lenzomj/conan-libfreenect"
    description = "libfreenect is a userspace driver for the Microsoft Kinect"
    topics = ("kinect", "opencv", "driver")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"

    source_dir = "libfreenect"
    install_dir = "install"

    def source(self):
        self.run("git clone --branch %s https://github.com/OpenKinect/libfreenect.git" % self.version)
        tools.replace_in_file("%s/CMakeLists.txt" % self.source_dir,
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

        cmake.configure(source_dir='%s' % self.source_dir, build_dir='.')
        cmake.build()

    def package(self):
        self.copy('*.h', src='%s/include' % self.source_dir, dst='include/%s' % self.source_dir)
        self.copy('*.so', src='lib', dst='lib')

    def package_info(self):
        self.cpp_info.libs = ["freenect"]

