from setuptools import setup, find_packages
import numpy as np
import re

# auto-updating version code stolen from Orbitize
def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
                       open(project + '/__init__.py').read())
    return result.group(1)

def get_requires():
    reqs = []
    for line in open('requirements.txt', 'r').readlines():
        reqs.append(line)
    return reqs

def get_extensions():
    extensions = []
    return extensions

setup(
    name='TCalc',
    version=get_property('__version__', 'TCalc'),
    description='Telescope Calculator! A tool for your telescope',
    # long_description=("README.md").read_text(),
    # long_description_content_type="text/markdown",
    url='https://github.com/Bhavesh012/Telescope-Calculator',
    author='Bhavesh Rajpoot, Ryan Keenan, Binod Bhattarai, Dylon Benton',
    author_email='',
    license='MIT',
    packages=find_packages(),
    ext_modules=get_extensions(),
    include_dirs=[np.get_include()],
    include_package_data = True,
    zip_safe=False,
    classifiers=[
        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
        ],
    keywords='Telescopes Astronomy Eyepiece Magnification',
    install_requires=get_requires()
    )