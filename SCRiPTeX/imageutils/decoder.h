#include <string>
#include <vector>
#include <Magick++.h>

using namespace std;
using namespace Magick;


// Decoder object must be instantiated with a path to an image.
class Decoder {

    private:
        vector<vector<int>> blackwhite; // integer values of the pixels
        int width = 0; // number of columns in image
        int height = 0; // number of rows in image
        int xtrim = 0;
        int ytrim = 0;
        void decodeImage(Image, bool);

    public:
        Decoder(vector<string>); // initializes the class with paths to images
        Decoder(vector<string>, bool); // initializes with path and if grid paper
        vector<vector<int>> getImage(); // return the raw image as a columns*rows array
};


// Decoder Method Implementations

// initializes the class with path to image
// assumes no blue lines on page
Decoder::Decoder(vector<string> images) : Decoder(images, false) {}

// initializes the class with path to image
Decoder::Decoder(vector<string> images, bool blueLines) {
    unsigned int inWidth, inHeight;
    int numImages = images.size();
    for (int i = 0 ; i < numImages ; i++) {
        Image temp(images[i]);
        if (width == 0 || height == 0) { // set widths
            inWidth = temp.columns();
            inHeight = temp.rows();
            xtrim = int(width*0.05);
            ytrim = int(height*0.05);
            width = inWidth - 2*xtrim;
            height = inHeight - 2*ytrim;
        } else if (temp.columns() != inWidth || temp.rows() != inHeight) {
            // resize if necessary, assume same aspect
            temp.resize(Geometry(to_string(inWidth) + "x" + to_string(inHeight) + "!"));
        }
        temp.crop(Geometry(width, height, xtrim, ytrim));
        decodeImage(temp, blueLines);
    }
}

// return the raw image as a row*column vector
vector<vector<int>> Decoder::getImage() {
    return blackwhite;
}

// ignore blueLines it is developement feature
void Decoder::decodeImage(Image image, bool blueLines) {
    int r, g, b, value, thresh;
    vector<int> values;

    // depending on 32 vs 64 bit, pixels are less/more "accurate"
    float quantumRange = pow(2, image.modulusDepth());

    // get a "pixel cache" for the entire image
    PixelPacket* pixels = image.getPixels(0, 0, width, height);
    
    // find threshold
    r = (int)(((Color)pixels[0]).redQuantum() / quantumRange);
    g = (int)(((Color)pixels[0]).greenQuantum() / quantumRange);
    b = (int)(((Color)pixels[0]).blueQuantum() / quantumRange);
    
    thresh = int(((r + g + b) / 6)*1.5);

    r = (int)(((Color)pixels[width-1]).redQuantum() / quantumRange);
    g = (int)(((Color)pixels[width-1]).greenQuantum() / quantumRange);
    b = (int)(((Color)pixels[width-1]).blueQuantum() / quantumRange);

    value = int(((r + g + b) / 6)*1.5);
    if (thresh < value) thresh = value;

    r = (int)(((Color)pixels[(width-1)*(height-2) + 1]).redQuantum() / quantumRange);
    g = (int)(((Color)pixels[(width-1)*(height-2) + 1]).greenQuantum() / quantumRange);
    b = (int)(((Color)pixels[(width-1)*(height-2) + 1]).blueQuantum() / quantumRange);

    value = int(((r + g + b) / 6)*1.5);
    if (thresh < value) thresh = value;

    r = (int)(((Color)pixels[(width-1)*(height-1)]).redQuantum() / quantumRange);
    g = (int)(((Color)pixels[(width-1)*(height-1)]).greenQuantum() / quantumRange);
    b = (int)(((Color)pixels[(width-1)*(height-1)]).blueQuantum() / quantumRange);

    value = int(((r + g + b) / 6)*1.5);
    if (thresh < value) thresh = value;

    // Extract RGB Values
    for (int row = 0 ; row < height ; row++) {
        for (int column = 0 ; column < width ; column++) {
            // get [0..255] RGB values
            r = (int)(((Color)pixels[column + row*width]).redQuantum() / quantumRange);
            g = (int)(((Color)pixels[column + row*width]).greenQuantum() / quantumRange);
            b = (int)(((Color)pixels[column + row*width]).blueQuantum() / quantumRange);
            
            value = (r + g + b) / 3;

            if (blueLines && (b - 10) > g && (b - 35) > r) {
                values.push_back(1);
            } else {
                if (value > thresh) {
                    values.push_back(1);
                } else {
                    values.push_back(0);
                }
            }
        }
        blackwhite.push_back(values);
        values.clear();
    }
}