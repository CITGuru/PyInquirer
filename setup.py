from setuptools import setup, find_packages
from io import open
from os import path
import atexit
here = path.abspath(path.dirname(__file__))

# long description from the README file

def make_url(text, link):
    return "\x1b]8;;"+link+"\a"+text+"\x1b]8;;\a"

def _post_install():
    print('\033[0J')
    print('\033[1;34;40m Thanks for using PyInquirer.')
    open_collective_url = make_url("OpenCollective", "http://opencollective.com/pyinquirer")
    pyinquirer_url = make_url("PyInquirer", "http://github.com/citguru/pyinquirer")
    pr_url = make_url('PR', "http://github.com/citguru/pyinquirer/pulls")
    author_url = make_url("Oyetoke Toby", "http://citguru.github.io")
    print('\033[1;34;40m Support us at ' + open_collective_url +' to keep the community growing.')
    print('\033[1;34;40m You can also contribute to ' + pyinquirer_url + ' by sending a ' + pr_url)
    print('\033[1;32;40m Author: ' + author_url + ' and other wonderful contributors.\n I am also looking for work, contact me at oyetoketoby80@gmail.com.')


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]

setup(
    name='PyInquirer',
    version='1.0.4',
    description=(
          'A Python module for collection of common interactive command line user interfaces,'
          ' based on Inquirer.js'
    ),
    long_description=long_description,
    license='MIT',
    url='https://github.com/CITGuru/PyInquirer/',
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


atexit.register(_post_install)