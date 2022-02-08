from setuptools import setup

VERSION = (0, 2, 0)

def version():
    v = ".".join(str(v) for v in VERSION)
    cnt = f'__version__ = "{v}" \n__version_full__ = __version__'
    with open('pslog/version.py', 'w') as f:
        f.write(cnt)
    return v

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pslog",
    version=version(),
    author="Mattia Bruno",
    author_email="mattia.bruno@cern.ch",
    description="A Python utility to create Postscript log files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mbruno46/pslog.git",
    packages=['pslog'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPLv2",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
)