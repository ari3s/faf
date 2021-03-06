#!/usr/bin/python
#
# Copyright (C) 2018  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README")) as fd:
    README = fd.read()

three_up = os.path.abspath(os.path.join(__file__, "../../.."))
with open(os.path.join(three_up, "faf-version")) as fver:
    VERSION = fver.read()

setup(
    name="faf_schema",
    version=VERSION,
    description="A schema package for messages sent by FAF",
    long_description=README,
    url="https://github.com/abrt/faf/",
    # Possible options are at https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    license="GPLv3+",
    maintainer="ABRT Team",
    maintainer_email="crash-catcher@lists.fedorahosted.org",
    platforms=["Fedora", "GNU/Linux"],
    keywords="fedora",
    packages=find_packages(exclude=("faf_schema.tests", "faf_schema.tests.*")),
    include_package_data=True,
    zip_safe=False,
    install_requires=["fedora_messaging"],
    test_suite="faf_schema.tests",
    entry_points={
        "fedora.messages": [
            "faf.FafReportMessage=faf_schema.schema:FafReportMessage",
            "faf.FafProblemMessage=faf_schema.schema:FafProblemMessage",
        ]
    },
)
