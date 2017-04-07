#include <string>
#include <Magick++.h>

using namespace std;
using namespace Magick;


// imageresizer module of the SCRiPTeX application.
//
// Leverages Magick++ to resize the passed image.
//
// Compiled via:
//  g++ -fPIC -shared `Magick++-config --cppflags --cxxflags --ldflags --libs` -o normalizer.so normalizer.cpp


extern "C" void normalizeImage(char* image) {
    string imgStr = string(image);
    Image normalized(imgStr);
    normalized.magick("PBM");
    normalized.resize(Geometry("32x32!"));
    normalized.negate(true);
    normalized.compressType(NoCompression);
    normalized.write(imgStr.substr(0, imgStr.length()-4) + ".pbm");
}
