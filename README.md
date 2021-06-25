# TCalc: Telescope-Calculator

TCalc is a general toolkit designed for all the telescope owners and enthusiasts! This package has a set of functions that will allow you to calculate basic properties and performance of your telescope and eyepiece pair.

[![PyPI version](https://badge.fury.io/py/TCalc.svg)](https://badge.fury.io/py/TCalc)
[![Documentation Status](https://readthedocs.org/projects/tcalc/badge/?version=latest)](https://tcalc.readthedocs.io/en/latest/?badge=latest)
[![Requirements Status](https://requires.io/github/Bhavesh012/TCalc/requirements.svg?branch=main)](https://requires.io/github/Bhavesh012/TCalc/requirements/?branch=main)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Python application](https://github.com/Bhavesh012/TCalc/actions/workflows/python-app.yml/badge.svg)](https://github.com/Bhavesh012/TCalc/actions/workflows/python-app.yml)

<!-- add badges from pypistats, travis.ci, coveralls.io -->

TCalc has taken birth from the project task of Code/Astro Workshop 2021 hosted by Grad students of Caltech. The authors of this project are Bhavesh Rajpoot, Ryan Keenan, Binod Bhattarai and Dylon Benton. 
The package aims to save time and money for all the telescope owners and enthusiasts by telling them the overall configuration of their instrument and suggesting them optimal accessories for their telescope.

## Documentation

Docmentation is available [here.](https://tcalc.readthedocs.io/en/latest/?badge=latest) <!-- (http://radvel.readthedocs.io/) -->

## Getting Started

### Installation

TCalc is a cross-platform python package and works on almost every OS. There are two ways to install the package:

#### Using `pip`:
```python
pip install tcalc
```

#### Using GitHub:
```python
git clone https://github.com/Bhavesh012/TCalc.git
cd TCalc
pip install -e .
```

### Basic Usage
```python
$ from TCalc.tcalc import telescope, eyepiece
$ my_telescope = telescope(D_o = 203.2, f_o = 2032)
$ eyepiece1 = eyepiece(f_e = 25, fov_e = 52)
$ my_telescope.add_eyepiece(eyepiece1,select=True)
$ my_telescope.say_configuration()
```
```
   The telescope has the following layout:
      Aperture diameter: 203.2 mm
      Focal length: 2032 mm, corresponding to a focal ratio of 10.0

   In good atmospheric conditions, the resolution of the telescope (Dawes limit) is 0.6 arcseconds
   By wavelength, the resolution is
      400 nm (blue): 0.5 arcsec
      550 nm (green): 0.7 arcsec
      700 nm (red): 0.9 arcsec

   The maximum possible magnification factor is 406.4
   This means the minimum compatible eyepiece focal length is 5.0 mm

   The minimum magnification factor and corresponding maximum eyepiece focal length depend on the diameter of the observer's eye.
   For a telescope user with an eye diameter of 7 mm (apropriate for an age around 25 years):
      The minimum magnification factor is 29.0
      This means the maximum compatible eyepiece focal length is 406.4 mm

   The faintest star that can be seen by this telescope is 13.5 mag

   The currently selected eyepiece is 'omni_25', which has the following layout:
      Focal length: 25 mm
      Field of view: 52 degrees

   With this eyepiece:
      The magnification factor is 81.3. This is compatible with the telescope limits.
      The true field of view is 1 degrees
      The exit pupil diameter is 2.5 mm

   The faintest surface brightness that can be seen by this telescope is 12.50
```

### Tutorials
['Base Tutorial'](\docs\tutorials\TCalc_tutorial.ipynb)
