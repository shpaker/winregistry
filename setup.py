from setuptools import setup
# import os


# def read(fname):
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup (
    name='winregistry',
    version='0.8.2',
    author='Alexander Shpak',
    author_email='shpaker@gmail.com',
    description=('Library aimed at working with Windows registry'),
    # long_description=read('readme.rst'),
    keywords='windows registry regedit winreg',
    url='https://github.com/shpaker/winregistry',
    platforms='windows',
    packages=['winregistry', 'winregistry.robot'],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Framework :: Robot Framework :: Library',
        'Environment :: Win32 (MS Windows)',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: Microsoft :: Windows'
    ]
)