#!/usr/bin/env python
"""The setup script."""

import os

from setuptools import find_packages, setup


def parse_requirements(path):
    """Parse ``requirements.txt`` at ``path``."""
    requirements = []
    with open(path, "rt") as reqs_f:
        for line in reqs_f:
            line = line.strip()
            if line.startswith("-r"):
                fname = line.split()[1]
                inner_path = os.path.join(os.path.dirname(path), fname)
                requirements += parse_requirements(inner_path)
            elif line != "" and not line.startswith("#"):
                requirements.append(line)
    return requirements


with open("README.md") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.md") as history_file:
    history = history_file.read()

test_requirements = parse_requirements("requirements/test.txt")
install_requirements = parse_requirements("requirements/base.txt")


package_root = os.path.abspath(os.path.dirname(__file__))
version = {}
with open(os.path.join(package_root, "clinvar_this/_version.py")) as fp:
    exec(fp.read(), version)
version = version["__version__"]

setup(
    author="Manuel Holtgrewe",
    author_email="manuel.holtgrewe@bih-charite.de",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="ClinVar Submission via API Made Easy",
    entry_points={"console_scripts": ["clinvar-this=clinvar_this.cli:cli"]},
    install_requires=install_requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="clinvar",
    name="clinvar-this",
    packages=find_packages(
        include=[
            "clinvar_this",
            "clinvar_this.*",
            "clinvar_api",
            "clinvar_api.*",
            "clinvar_data",
            "clinvar_data.*",
        ]
    ),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/bihealth/clinvar-this",
    version=version,
    zip_safe=False,
)
