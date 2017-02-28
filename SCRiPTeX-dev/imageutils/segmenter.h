// Compiled via:
//  g++ -fPIC -shared `Magick++-config --cppflags --cxxflags --ldflags --libs` -o imagedecoder.so imagedecoder.cpp


#include <iostream>
#include <stdio.h>
#include <fstream>
#include <vector>
#include <complex>
#include <queue>
#include <sstream>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <string>
#include <cstring>

#include "decoder.h"

using namespace std;


// flags
bool makePGM;
bool statusUpdates;
// queue of spaces (FIFO)
queue<char> listSpaces;

string characterIndex; // char positional index
queue<vector<vector<int>>> listChars; // queue of segmented chars
char* indexArr;


class Segmenter {
    public:
        Segmenter(string);
        string getIndex();
    private:
        vector<vector<int>> decode(string);
        void segment(vector<vector<int>>);
        void segmentIntoChars(vector<vector<int>>);
        void segmentIntoLines(vector<vector<int>>);
        int findHorThreshold(vector<vector<int>>);
        int findVerThreshold(vector<vector<int>>);
        vector<vector<int>> bwify(vector<vector<int>>);
        vector<int> findHorDistribution(vector<vector<int>>, int);
        vector<int> findVerDistribution(vector<vector<int>>, int);
        void normalizeAspect(vector<vector<int>>&);
        void affixWhiteRows(vector<vector<int>>&, int);
        void affixWhiteCols(vector<vector<int>>&, int);
        int findBackgroundColor(vector<vector<int>>&);
        int findAvgCharWidth(vector<vector<int>>&, int);
        void findCharIndex(vector<vector<int>>&, int);
        string genIndex(queue<char>);
        vector<vector<int>> fileToArray(string);
        void writeToFile(queue<vector<vector<int>>>&, string);
        void writePGM(vector<vector<int>>&);
        void writeIndex(queue<char>&, string);
        void printDist(vector<int>&);
        void printVector(vector<vector<int>>&);
};

extern "C" {
    Segmenter* getSegmenterInstance(char* image) {
        return new Segmenter(string(image));
    }

    char* getIndex(Segmenter* instance) {
        string theIndex = instance->getIndex();
        int size = strlen(theIndex.c_str());
        indexArr = new char[size];
        for (int i = 0 ; i < size ; i++) {
            indexArr[i] = theIndex.c_str()[i];
        }
        return indexArr;
    }

    void destroySegmenterInstance(Segmenter* instance) {
        delete[] indexArr;
        delete instance;
    }
}



