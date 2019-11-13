from setuptools import setup, find_packages
import sys

sys.path.append('./builder')
sys.path.append('./tests')

from builder import __VERSION__

setup(
        name = 'StoryBuilder',
        version = __VERSION__,
        description = "This is a tool for construct a story",
        packages = find_packages(),
        test_suite = 'test_all.suite'
)
