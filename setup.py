from setuptools import setup, find_packages
import sys

sys.path.append('./builder')
sys.path.append('./tests')
sys.path.append('./utils')

from builder import __DESC__, __TITLE__, __VERSION__

setup(
        name = __TITLE__,
        version = __VERSION__,
        description = __DESC__,
        packages = find_packages(),
        test_suite = 'test_all.suite'
)
