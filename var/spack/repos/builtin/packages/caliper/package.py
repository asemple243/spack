# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import sys


class Caliper(CMakePackage):
    """Caliper is a program instrumentation and performance measurement
    framework. It provides data collection mechanisms and a source-code
    annotation API for a variety of performance engineering use cases,
    e.g., performance profiling, tracing, monitoring, and
    auto-tuning.
    """

    homepage = "https://github.com/LLNL/Caliper"
    git      = "https://github.com/LLNL/Caliper.git"

    version('master')
    version('1.7.0', tag='v1.7.0')
    # version 1.6.0 is broken b/c it downloads the wrong gotcha version
    version('1.6.0', tag='v1.6.0')

    is_linux = sys.platform.startswith('linux')

    variant('mpi', default=True,
            description='Enable MPI wrappers')
    variant('dyninst', default=False,
            description='Enable symbol translation support with dyninst')
    # libunwind has some issues on Mac
    variant('callpath', default=sys.platform != 'darwin',
            description='Enable callpath service (requires libunwind)')
    # pthread_self() signature is incompatible with PAPI_thread_init() on Mac
    variant('papi', default=sys.platform != 'darwin',
            description='Enable PAPI service')
    variant('libpfm', default=is_linux,
            description='Enable libpfm (perf_events) service')
    # gotcha doesn't work on Mac
    variant('gotcha', default=sys.platform != 'darwin',
            description='Enable GOTCHA support')
    variant('sampler', default=is_linux,
            description='Enable sampling support on Linux')
    variant('sosflow', default=False,
            description='Enable SOSflow support')

    depends_on('gotcha@1.0:', when='+gotcha')
    depends_on('dyninst', when='+dyninst')
    depends_on('papi', when='+papi')
    depends_on('libpfm4', when='+libpfm')
    depends_on('mpi', when='+mpi')
    depends_on('unwind', when='+callpath')
    depends_on('sosflow', when='+sosflow')

    depends_on('cmake', type='build')
    depends_on('python', type='build')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DBUILD_TESTING=Off',
            '-DBUILD_DOCS=Off',
            '-DWITH_DYNINST=%s'  % ('On' if '+dyninst'  in spec else 'Off'),
            '-DWITH_CALLPATH=%s' % ('On' if '+callpath' in spec else 'Off'),
            '-DWITH_GOTCHA=%s'   % ('On' if '+gotcha'   in spec else 'Off'),
            '-DWITH_PAPI=%s'     % ('On' if '+papi'     in spec else 'Off'),
            '-DWITH_LIBPFM=%s'   % ('On' if '+libpfm'   in spec else 'Off'),
            '-DWITH_SOSFLOW=%s'  % ('On' if '+sosflow'  in spec else 'Off'),
            '-DWITH_SAMPLER=%s'  % ('On' if '+sampler'  in spec else 'Off'),
            '-DWITH_MPI=%s'      % ('On' if '+mpi'      in spec else 'Off'),
            '-DWITH_MPIT=%s' % ('On' if spec.satisfies('^mpi@3:') else 'Off')
        ]

        if '+gotcha' in spec:
            args.append('-DUSE_EXTERNAL_GOTCHA=True')
        if '+papi' in spec:
            args.append('-DPAPI_PREFIX=%s'    % spec['papi'].prefix)
        if '+libpfm' in spec:
            args.append('-DLIBPFM_INSTALL=%s' % spec['libpfm4'].prefix)
        if '+sosflow' in spec:
            args.append('-DSOS_PREFIX=%s'     % spec['sosflow'].prefix)
        if '+callpath' in spec:
            args.append('-DLIBUNWIND_PREFIX=%s' % spec['libunwind'].prefix)

        if '+mpi' in spec:
            args.append('-DMPI_C_COMPILER=%s' % spec['mpi'].mpicc)
            args.append('-DMPI_CXX_COMPILER=%s' % spec['mpi'].mpicxx)

        return args
