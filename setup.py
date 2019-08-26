from setuptools import setup, find_packages

setup(
    name='terminal_utils',
    version='0.9.1',
    url='https://github.com/vphpersson/terminal_utils',
    author='vph',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.7'
)
