# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import setup, find_packages

import versioneer

setup(
    name="q2-pepsirf",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    author="Zane Fink",
    author_email="zwf5@nau.edu",
    description="QIIME 2 plugin for pepsirf.",
    license='BSD-3-Clause',
    url="",
    entry_points={
        "qiime2.plugins":
        ["q2-pepsirf=q2_pepsirf.plugin_setup:plugin"]
    },
    package_data={
        'q2_vsearch': ['citations.bib'],
        zip_safe=False,
    )
