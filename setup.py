from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup (
    name='winregistry',
    version='0.7',
    author='Alexander Shpak',
    author_email='shpaker@gmail.com',
    description=('Library aimed at working with Windows registry'),
    keywords='windows registry regedit winreg',
    url='https://github.com/shpaker/winregistry',
    packages=['winregistry'],
    platforms='windows',
    long_description=read('README.rst'),
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: Microsoft :: Windows'
    ]
)