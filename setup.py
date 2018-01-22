# -*- coding: utf-8 -*-

from os.path import join
from setuptools import setup, find_packages

version = '0.3'
readme = open('README.txt').read()
history = open(join('docs', 'HISTORY.txt')).read()


install_requires = [
    'sqlalchemy',  # While not used directly, can't work without it.
    'zope.interface',
    'zope.location',
    ]


tests_require = [
    'pytest',
    ]


setup(name='dolmen.sqlcontainer',
      version=version,
      description="Container abstraction for SQLAlchemy",
      long_description="%s\n\n%s\n" % (readme, history),
      keywords='Dolmen Container SQLAlchemy',
      author='The Dolmen team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://gitweb.dolmen-project.org',
      license='ZPL 2.1',
      namespace_packages=['dolmen'],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      classifiers=[
          'Environment :: Web Environment',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
