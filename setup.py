import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='tsbc-nc-auat',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    description='Automated User Acceptance Tests (AUAT) for Technical Safety BC'
                ' HTTP REST APIs.',
    long_description=README,
    author='Technical Safety BC',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing :: Acceptance',
        'Topic :: Software Development :: Testing :: BDD',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'behave',
        'requests',
        'htmlmin',
        'tox',
        'dgs==0.2.0',
    ],
    dependency_links=[
        'git+https://jdunham@bitbucket.safetyauthority.ca/scm/nc/document-generator-service.git@2a3c04e#egg=dgs-0.2.0',
    ],
    entry_points={
        'console_scripts': [
            'dgs-client = templateapi.scripts.client:main',
            'dgs-templates = templateapi.templates.templates:main',
        ],
    },
)
