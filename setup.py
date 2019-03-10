from distutils.core import setup

setup(
    name='BibTeXMagic',
    version='0.2 alpha',
    author='Piotr Bajger',
    author_email='piotr.bajger@hotmail.com',
    packages=['bibtexmagic', 'bibtexmagic.fields'],
    url='https://github.com/piotrbajger/bibtexmagic',
    license='LICENSE.txt',
    description='BibTeX parser in Python.',
    long_description=open('README.md').read(),
)
