from setuptools import setup, find_packages
from io import open
from os import path

here = path.abspath(path.dirname(__file__))

# get the dependencies
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' in x]

setup(
    name='PyInquirer',
    version='1.0.3',
    description=(
          'A Python module for collection of common interactive command line user interfaces,'
          ' based on Inquirer.js'
    ),
    license='MIT',
    url='https://github.com/CITGuru/PyInquirer/',
    python_requires=">=3.6.1",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: '
        'Libraries :: Application Frameworks',
    ],
    keywords='click, prompt-toolkit, cli, command-line, commandline, command-line-interface, python-inquiry, inquirer',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Oyetoke Toby',
    download_url='https://github.com/CITGuru/PyInquirer/archive/1.0.3.tar.gz',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='oyetoketoby80@gmail.com',
)
