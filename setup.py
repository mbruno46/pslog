from setuptools import setup, find_packages

VERSION = (0, 3, 0)

def version():
    v = ".".join(str(v) for v in VERSION)
    cnt = f'__version__ = "{v}" \n__version_full__ = __version__'
    with open('pslog/version.py', 'w') as f:
        f.write(cnt)
    with open('pslog/VERSION', 'w') as f:
        f.write(f'v{v}')
    return v

setup(
    name="pslog",
    version=version(),
    packages=find_packages(include=['pslog*']),
)
