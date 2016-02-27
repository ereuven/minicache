from distutils.core import setup
from sys import argv

dependencies = ['enum34']

setup(
    name='minicache',
    version='1.0',
    description='Python memory cache',
    author='Reuven',
    author_email='reuven@linux.com',
    url='',
    packages=['minicache'],
    requires=dependencies
)

try:
    if 'install' in argv:
        import pip
        [pip.main(['install', dep]) for dep in dependencies]
except:
    print "Can't find pip, please install dependencies manually."
    print 'Dependencies:', ','.join(dependencies)