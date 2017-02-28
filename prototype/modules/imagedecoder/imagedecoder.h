#ifndef IMAGEDECODER_H
#define IMAGEDECODER_H

#include <Magick++.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <stdlib.h>
#include <math.h>

using namespace std;
using namespace Magick;


class ImageDecoder{
    protected:
        string FileName;
        int rows, columns,r,g,b,threshold;
        bool lines = true;
    public:
        ImageDecoder(string infile, string outfile);
        void SetThreshold(int th);
        void SetFileName(string name);
        void SetRowCol(int x, int y);
        void ConvertImage(string output);
};

void _decodeImage(string, string);
extern "C" void decodeImage(char* infile, char* outfile) {
    _decodeImage(string(infile), string(outfile));
}

#endif