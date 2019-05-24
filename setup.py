import os
from setuptools import setup, find_packages

from friendship import VERSION


f = open(os.path.join(os.path.dirname(__file__), "README.md"))
readme = f.read()
f.close()

setup(
    name="django-friendship",
    version=".".join(map(str, VERSION)),
    description="django-friendship provides an easy extensible interface for following and friendship",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Frank Wiles",
    author_email="frank@revsys.com",
    url="https://github.com/revsys/django-friendship/",
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Framework :: Django",
    ],
    test_suite="runtests.runtests",
)
