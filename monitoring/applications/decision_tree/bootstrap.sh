#!/bin/bash

apt-get update && apt-get -qq -y install build-essential gfortran libopenblas-dev liblapack-dev
# apt-get install -qq -y python-tk libjpeg-dev zlib1g-dev
# python3 -m pip install Pillow matplotlib scikit-learn psutil tk pandas prettytable ipython h5py cairocffi
mkdir /home/kevin
touch /home/kevin/testtime.csv