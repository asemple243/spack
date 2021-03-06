# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


def check(condition, msg):
    """Raise an install error if condition is False."""
    if not condition:
        raise InstallError(msg)


class CmakeClient(CMakePackage):
    """A dumy package that uses cmake."""
    homepage  = 'https://www.example.com'
    url       = 'https://www.example.com/cmake-client-1.0.tar.gz'

    version('1.0', '4cb3ff35b2472aae70f542116d616e63')

    callback_counter = 0

    flipped = False
    run_this = True
    check_this_is_None = None
    did_something = False

    @run_after('cmake')
    @run_before('cmake', 'build', 'install')
    def increment(self):
        self.callback_counter += 1

    @run_after('cmake')
    @on_package_attributes(run_this=True, check_this_is_None=None)
    def flip(self):
        self.flipped = True

    @run_after('cmake')
    @on_package_attributes(does_not_exist=None)
    def do_not_execute(self):
        self.did_something = True

    def setup_environment(self, spack_env, run_env):
        spack_cc    # Ensure spack module-scope variable is avaiabl
        check(from_cmake == "from_cmake",
              "setup_environment couldn't read global set by cmake.")

        check(self.spec['cmake'].link_arg == "test link arg",
              "link arg on dependency spec not readable from "
              "setup_environment.")

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_cc    # Ensure spack module-scope variable is avaiable
        check(from_cmake == "from_cmake",
              "setup_dependent_environment couldn't read global set by cmake.")

        check(self.spec['cmake'].link_arg == "test link arg",
              "link arg on dependency spec not readable from "
              "setup_dependent_environment.")

    def setup_dependent_package(self, module, dspec):
        spack_cc    # Ensure spack module-scope variable is avaiable
        check(from_cmake == "from_cmake",
              "setup_dependent_package couldn't read global set by cmake.")

        check(self.spec['cmake'].link_arg == "test link arg",
              "link arg on dependency spec not readable from "
              "setup_dependent_package.")

    def cmake(self, spec, prefix):
        assert self.callback_counter == 1

    def build(self, spec, prefix):
        assert self.did_something is False
        assert self.flipped is True
        assert self.callback_counter == 3

    def install(self, spec, prefix):
        assert self.callback_counter == 4
        # check that cmake is in the global scope.
        global cmake
        check(cmake is not None, "No cmake was in environment!")

        # check that which('cmake') returns the right one.
        cmake = which('cmake')
        check(cmake.exe[0].startswith(spec['cmake'].prefix.bin),
              "Wrong cmake was in environment: %s" % cmake)

        check(from_cmake == "from_cmake",
              "Couldn't read global set by cmake.")

        check(os.environ['from_cmake'] == 'from_cmake',
              "Couldn't read env var set in envieonmnt by dependency")

        mkdirp(prefix.bin)
        touch(join_path(prefix.bin, 'dummy'))
