#!/usr/bin/env bash

g++ -Ofast -Wall -fPIC -shared -std=gnu++11 `Magick++-config --cppflags --cxxflags --ldflags --libs` -o imageutils/segmenter.so imageutils/segmenter.cpp
g++ -Ofast -Wall -fPIC -shared -std=gnu++11 `Magick++-config --cppflags --cxxflags --ldflags --libs` -o imageutils/normalizer.so imageutils/normalizer.cpp
