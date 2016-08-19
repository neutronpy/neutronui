#!/usr/bin/env python
"""NeutronUi: NeutronPy's Web-based UI App

NeutronPy is a collection of commonly used tools aimed at facilitating the
analysis of neutron scattering data. NeutronPy is built primarily using the
numpy and scipy python libraries, with a translation of ResLib 3.4c (MatLab)
routines for Instrument resolution calculations.

    Copyright (C) 2016 David M Fobes

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import os
import platform
import re
import sys
from glob import glob

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('neutronui/__init__.py') as f:
    __version__ = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M).group(1)

CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Science/Research
License :: OSI Approved :: MIT License
Natural Language :: English
Programming Language :: Python :: 3.5
Programming Language :: Python :: Implementation :: CPython
Topic :: Scientific/Engineering :: Physics
Operating System :: Microsoft :: Windows
Operating System :: POSIX :: Linux
Operating System :: Unix
Operating System :: MacOS :: MacOS X
"""

DOCLINES = __doc__.split("\n")
app = ['app/neutronui.py']
includes = ['PyQt4.QtCore', 'PyQt4.QtWebKit', 'PyQt4.QtGui']
excludes = ['PyQt4.QtDesigner', 'PyQt4.QtOpenGL', 'PyQt4.QtScript', 'PyQt4.QtSql', 'PyQt4.QtTest', 'PyQt4.QtXml',
            'PyQt4.phonon']
packages = ['neutronui']


def setup_package():
    r"""Setup package function
    """
    src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)

    if platform.system() == 'Darwin':
        options = dict(argv_emulation=True,
                       includes=includes,
                       excludes=excludes,
                       iconfile='app/neutronui.icns',
                       packages=['neutronui', 'flask', 'jinja2'],
                       site_packages=True,
                       plist=dict(CFBundleName='NeutronUI'),
                       )
        args = dict(app=app,
                    options=dict(py2app=options),
                    packages=packages,
                    package_data=dict(neutronui=['static/*', 'templates/*']),
                    setup_requires=['py2app'],
                    install_requires=['neutronpy'],
                    # data_files=[('', ['LICENSE', 'README.md']),
                    #             ('neutronui/templates', glob('neutronui/templates/*')),
                    #             ('neutronui/static', glob('neutronui/static/*'))],
                    )
    elif platform.system() == 'Windows':
        options = dict(includes=includes,
                       excludes=excludes,
                       dll_excludes=['MSVCP90.dll'],
                       skip_archive=True,
                       )
        args = dict(windows=[dict(script=app[0])],
                    options=dict(py2exe=options),
                    package_data=dict(neutronui=['static/*', 'templates/*']),
                    setup_requires='py2exe',
                    data_files=[('', ['LICENSE', 'README.md']),
                                ('neutronui/templates', glob('neutronui/templates/*')),
                                ('neutronui/static', glob('neutronui/static/*'))],
                    )
    else:
        args = dict(include_package_data=True,
                    scripts=app,
                    package_data=dict(neutronui=['static/*', 'templates/*']),
                    data_files=[('', ['LICENSE', 'README.md']),
                                ('neutronui/templates', glob('neutronui/templates/*')),
                                ('neutronui/static', glob('neutronui/static/*')),
                                ('/usr/share/applications', ['app/neutronui.desktop']),
                                ('/usr/share/pixmaps', ['app/neutronui.xpm'])]
                    )

    metadata = dict(name='neutronui',
                    version=__version__,
                    description=DOCLINES[0],
                    long_description="\n".join(DOCLINES[2:]),
                    author='David M Fobes',
                    maintainer='davidfobes',
                    download_url='https://github.com/neutronpy/neutronui/releases',
                    url='https://github.com/neutronpy/neutronui',
                    license='GPL v3',
                    platforms=["Windows", "Linux", "Mac OS X", "Unix"],
                    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
                    entry_points=dict(console_scripts=["neutronui=neutronui:launch"]),
                    **args
                    )

    try:
        setup(**metadata)
    finally:
        del sys.path[0]
        os.chdir(old_path)
    return


if __name__ == '__main__':
    setup_package()
