from setuptools import setup, find_packages
import sys

sys.path.append('./builder')
sys.path.append('./tests')

from builder import __DESC__, __TITLE__, __VERSION__

setup(
        name = __TITLE__,
        version = __VERSION__,
        description = __DESC__,
        packages = find_packages(),
        test_suite = 'all_tests.suite'
)
