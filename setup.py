from setuptools import setup, find_packages

setup(
    name='onvifWrap',
    version='0.1',
    packages=find_packages(),
    description='Una breve descrizione del tuo package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alessio Michelassi',
    author_email='alessio.michelassi@gmail.com',
    url='',
    install_requires=[
        # elenca qui le dipendenze del tuo package, ad esempio
        # 'numpy',
    ],
    classifiers=[
        # Classificatori per PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
