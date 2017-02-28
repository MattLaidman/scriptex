#!/usr/bin/env bash

g++ -g -Wall -fPIC -shared -std=gnu++11 `Magick++-config --cppflags --cxxflags --ldflags --libs` -o imageutils/segmenter.so imageutils/segmenter.cpp
g++ -g -Wall -fPIC -shared -std=gnu++11 `Magick++-config --cppflags --cxxflags --ldflags --libs` -o imageutils/resizer.so imageutils/resizer.cpp
