from setuptools import find_packages, setup


def get_requirements():
    with open('requirements.txt') as f:
        return f.readlines()


setup(
    name='tuitools',
    version='0.0',
    description='Templates for interactive input',
    author='J. M. F. Tsang',
    author_email='j.m.f.tsang@cantab.net',
    url='https://github.com/jftsang/tuitools',
    packages=find_packages(),
    entry_points={'console_scripts': ['tuitools=tuitools._example']},
    setup_requires=get_requirements()
)
