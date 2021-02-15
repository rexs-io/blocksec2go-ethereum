from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='blocksec2go-ethereum',
    version='0.2.0',
    description='Wrapper for blocksec2go allowing easy hardware-based signing of Ethereum transactions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rexs-io/blocksec2go-ethereum',
    author='rexs.io',
    license='ISC',
    author_email='dev@rexs.io',
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 3',
    ],
    keywords='ethereum blocksec2go hardware-signing hardware wallet',
    python_requires='>=3.0, <4',
    install_requires=[
        'blocksec2go==1.2',
        'ecdsa==0.15',
        'web3==5.6.0'
    ],
    packages=[
      'blocksec2go_ethereum'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/rexs-io/blocksec2go-ethereum/issues',
        'Source': 'https://github.com/rexs-io/blocksec2go-ethereum',
    },
)