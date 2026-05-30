"""
YGScript Installation and Package Setup
"""

from setuptools import setup, find_packages

setup(
    name='ygscript',
    version='1.0.0',
    description='A modern programming language with explicit types and clean syntax',
    author='YGstudio97',
    license='MIT',
    packages=find_packages(),
    package_dir={'': 'src'},
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'ygscript=ygscript:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
