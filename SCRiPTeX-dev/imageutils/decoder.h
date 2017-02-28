#include <string>
#include <vector>
#include <iostream>
#include <Magick++.h>

using namespace std;
using namespace Magick;


// Decoder object must be instantiated with a path to an image.
class Decoder {

    private:
        Image* image; // the image
        vector<vector<int>> greyscale; // integer values of the pixels
        int width; // number of columns in image
        int height; // number of rows in image
        void decodeImage(bool);

    public:
        Decoder(string); // initializes the class with path to image
        Decoder(string, bool); // initializes with path and if grid paper
        vector<vector<int>> getImage(); // return the raw image as a columns*rows array
};


// Decoder Method Implementations

// initializes the class with path to image
// assumes no blue lines on page
Decoder::Decoder(string image) : Decoder(image, false) {}

// initializes the class with path to image
Decoder::Decoder(string image, bool blueLines) {
    this->image = new Magick::Image(image);

    width = (this->image)->columns();
    height = (this->image)->rows();

    decodeImage(blueLines);
}

// return the raw image as a row*column vector
vector<vector<int>> Decoder::getImage() {
    return greyscale;
}

// ignore blueLines it is developement feature
void Decoder::decodeImage(bool blueLines) {
    int r, g, b;
    vector<int> values;
    
    // depending on 32 vs 64 bit, pixels are less/more "accurate"
    float quantumRange = pow(2, (this->image)->modulusDepth());

    // get a "pixel cache" for the entire image
    PixelPacket* pixels = (this->image)->getPixels(0, 0, width, height);

    // Extract RGB Values
    for (int column = 0 ; column < width ; column++) {
        for (int row = 0 ; row < height ; row++) {
            // get [0..255] RGB values
            r = (int)(((Color)pixels[column + row*width]).redQuantum() / quantumRange);
            g = (int)(((Color)pixels[column + row*width]).greenQuantum() / quantumRange);
            b = (int)(((Color)pixels[column + row*width]).blueQuantum() / quantumRange);
            if (blueLines && (b - 10) > g && (b - 35) > r) {
                values.push_back(250);
            } else {
                values.push_back((int)((r + g + b) / 3));
            }
        }
        greyscale.push_back(values);
        values.clear();
    }
}