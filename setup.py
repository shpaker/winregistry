from setuptools import setup
from os.path import join, dirname

setup (
    name='winregistry',
    version='0.7',
    author='Alexander Shpak',
    author_email='shpaker@gmail.com',
    description=('Library aimed at working with Windows registry'),
    keywords='windows registry regedit winreg',
    url='https://github.com/shpaker/winregistry',
    packages=['winregistry'],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: Microsoft :: Windows'
    ]
)