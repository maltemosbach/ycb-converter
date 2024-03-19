import pathlib
from setuptools import setup


def parse_requirements(filename):
    requirements = pathlib.Path(filename)
    requirements = requirements.read_text().split('\n')
    requirements = [x for x in requirements if x.strip()]
    return requirements


setup(
    name='ycb_converter',
    version='0.1.0',
    description='',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    author='Malte Mosbach',
    packages=['ycb_converter'],
    install_requires=parse_requirements('requirements.txt'),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)