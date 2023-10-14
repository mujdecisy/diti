import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="diti",
    version="0.0.1",
    description="diti to reduce your datetime operation pains",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mujdecisy/diti",
    keywords=["python", "diti", "datetime", "timezone"],
    author="mujdecisy",
    author_email="mujdecisy@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=["diti"],
    include_package_data=True,
    install_requires=["pytz"]
)