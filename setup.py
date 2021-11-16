from setuptools import setup, find_packages
import re
import os

def get_version(package):
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)

def get_long_description():
    with open("README.md", encoding="utf8") as f:
        return f.read()

setup(
    name="periodic_table_tui",
    version=get_version("periodic_table_tui"),
    url="https://github.com/pryme-svg/periodic-table-tui",
    license="GPL3",
    license_files = ('LICENSE',),
    author="pryme-svg",
    author_email="edoc.www@gmail.com",
    description="A periodic table for the command line",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=find_packages(),
    keywords=['periodic_table'],
    entry_points={"console_scripts": ["periodic_table_tui=periodic_table_tui.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False
)
