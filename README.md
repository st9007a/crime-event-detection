# Crime Event Detection

## Install Packages

`pip3 install -r requires.txt`

## Build Features

`cd tools`
`python3 make_positive.py`
`python3 make_negative.py`
`python3 make_features.py` # Need about 20 ~ 30 minutes
`cd ..`

## Train

`python3 train.py`

## Issues

- Location category by grid map in `make_negative.py`
- Multiclass classification
  - Merge some labels
- Merge location categories
 - reference: https://developer.foursquare.com/docs/resources/categories
