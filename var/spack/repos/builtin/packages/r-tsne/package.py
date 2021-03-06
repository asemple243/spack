# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTsne(RPackage):
    """A "pure R" implementation of the t-SNE algorithm."""

    homepage = "https://cran.r-project.org/web/packages/tsne/index.html"
    url      = "https://cran.r-project.org/src/contrib/tsne_0.1-3.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/tnse"

    version('0.1-3', '00974d4b3fd5f1100d0ebd24e03b0af9')
    version('0.1-2', 'd96d8dce6ffeda68e2b25ec1ff52ea61')
    version('0.1-1', '8197e5c61dec916b7a31b74e658b632d')

    depends_on('r@3.4.0:3.4.9')
