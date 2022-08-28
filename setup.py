# setup.py
from setuptools import setup, find_packages
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path("database/version.py")
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name="Share Tracker",
    author="Andy Blight",
    install_requires=["pandas", "xlrd"],
    url="https://github.com/andyblight/share-tracking-1",
    version=main_ns["__version__"],
)
