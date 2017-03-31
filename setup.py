from setuptools import setup
from setuptools import find_packages

def readme():
    with open('README.md', 'r') as f:
        return f.read()

setup(
    name = 'pyqremis',
    description = 'Library code implementing the qremis metadata standard',
    long_description = readme(),
    author = "Brian Balsamo",
    author_email = "balsamo@uchicago.edu",
    packages = find_packages(
        exclude = [
            "build",
            "dist"
        ]
    ),
)
