import os
import pathlib
from typing import Any, Dict, cast

from setuptools import find_packages, setup


def get_version(version_file: "os.PathLike[str]") -> str:
    locls: Dict[str, Any] = {}
    exec(open(version_file).read(), {}, locls)
    return cast(str, locls["__version__"])


here = pathlib.Path(__file__).parent.resolve()

readme_file = here / "README.md"
long_description = readme_file.read_text(encoding="utf-8")

version_file = here / "src" / "hdltypes" / "version.py"
version = get_version(version_file)

setup(
    name="hdltypes",
    version=version,
    description="Models of VHDL datatypes in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ktbarrett/pyhdltypes",
    author="Kaleb Barrett",
    author_email="dev.ktbarrett@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={"hdltypes": ["py.typed"]},
    python_requires=">=3.6, <4",
    install_requires=[],
    entry_points={},
    zip_safe=False,
)
