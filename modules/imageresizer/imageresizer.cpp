#include <string>
#include <Magick++.h>

using namespace std;
using namespace Magick;


// imageresizer module of the SCRiPTeX application.
//
// Leverages Magick++ to resize the passed image.
//
// Compiled via:
//  g++ -fPIC -shared `Magick++-config --cppflags --cxxflags --ldflags --libs` -o imageresizer.so imageresizer.cpp


extern "C" void resizeImage(char* image) {
    string imgStr = string(image);
    Image resized(imgStr);
    resized.resize(Geometry("32x32!"));
    resized.compressType(NoCompression);
    resized.write(imgStr);
}
