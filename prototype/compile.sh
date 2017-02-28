#!/usr/bin/env bash

g++ -fPIC -shared -std=gnu++11 `Magick++-config --cppflags --cxxflags --ldflags --libs` -o modules/imagedecoder/imagedecoder.so modules/imagedecoder/imagedecoder.cpp
g++ -fPIC -shared -std=gnu++11 `Magick++-config --cppflags --cxxflags --ldflags --libs` -o modules/imageresizer/imageresizer.so modules/imageresizer/imageresizer.cpp
g++ -fPIC -shared -std=gnu++11 -o modules/imagesegmentation/imagesegmentation.so modules/imagesegmentation/imagesegmentation.cpp
