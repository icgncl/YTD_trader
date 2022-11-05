import os

from setuptools import find_packages, setup


# setuptools doesn't support recursive package_data out-of-box,
# so we need to find them ourselves
def package_files(directory):
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            yield os.path.join("../..", path, filename)


version = "0.0.1"

setup(
    name="cassandra_dashboard",
    version=version,
    description="Cassandra Dashboard",
    classifiers=[
        "Programming Language :: Python",
    ],
    keywords="DI-502",
    author="YTD",
    author_email="ytdmetu@gmail.com",
    url="https://github.com/icgncl/YTD_trader/dashboard",
    license="UNLICENSED",
    packages=find_packages(),
    zip_safe=False,
    python_requires=">=3.8.0",
)
