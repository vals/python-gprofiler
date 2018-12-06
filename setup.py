''' Setup file for python-gprofiler
'''

from setuptools import setup, find_packages

setup(
        name='gprofiler',
        version='1.2.1',
        description='Python port of the R wrapper for the g:Profiler functional enrichment tool.',
        packages=find_packages(),
        install_requires=['requests', 'pandas'],
        url='https://github.com/vals/python-gprofiler',
        author='Valentine Svensson',
        author_email='valentine@nxn.se'
    )
