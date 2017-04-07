#include <iostream>
#include <stdio.h>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <sys/stat.h>
#include <sys/types.h>
#include <string>
#include <list>
#include <math.h>
#include <cstring>
#include "decoder.h"

using namespace std;

/* CharacterData class, represents the characteristics
 * of a segmented character alongside the pixel data of
 * said character. */
class CharacterData {
	private:
		vector<vector<int> > pixelData; // pixel values
		int area; // area of character
		int position[2]; // position of character
		int line; // line it was found on
		int rindex; // R-Index value
		int srindex; // SR-Index value
		int sindex; // degree of scripting
	public:	
		CharacterData() {} // constructor
		virtual ~CharacterData() {} // deconstructor
		/* main setter */
		void setPixels(vector<vector<int> > in, int pos[2], int ar, int li, int r, int sr) {
			pixelData = in;
			area = ar;
			position[0] = pos[0]; position[1] = pos[1];
			line = li;
			rindex = r, srindex = sr, sindex = 0;
		}
		void setPixels(vector<vector<int> > in) { // setter function for pixel data
			pixelData = in;
		}
		vector<vector<int> > &getPix() { // mutator function for pixel data
			return pixelData;
		}
		int getArea() { // getter function for area
			return area;
		}		
		int getWidth() { // getter function for character width
			return pixelData.size();
		}
        int getHeight() { // getter function for character height
            return getArea() / getWidth();
        }
		int getLine() { // getter function for line number
			return line;
		}
		int* getPos() { // getter function for character position
			return position;
		}
		int getS() { // getter function for script degree
			return sindex;
		}
		void setS(int in) { // setter function for script degree
			sindex = in;
		}		
		int getR() { // getter function for R-Index value
			return rindex;
		}
		int getSR() { // getter function for SR-Index value
			return srindex;
		}
};

class Segmenter {
    public:
        Segmenter(string);
        string getNSIndex();
        string getSIndex();
        string getRIndex();
        string getSRIndex();
    private:
        // I/O
        vector<vector<int> > decodeImage(string);
        vector<vector<int> > fileToArray(string);
        void writePGM(vector<vector<int> >&, int, int);
        // segmentation functions
        void segmentHandler(vector<vector<int> >&);
        void segmentIntoLines(vector<vector<int> >&, unsigned int, unsigned int, unsigned int);
        void segmentIntoChars(vector<vector<int> >&, unsigned int, unsigned int, unsigned int);
        // functions for index generation
        void indexHandler(list<CharacterData>&);
        void createNSIndex(CharacterData&, CharacterData&);
        void createRIndex(CharacterData&);
        void createSIndex(CharacterData&, CharacterData&, CharacterData&);
        void createSRIndex(CharacterData&);
        // for cleaning up image/slight processing
        void postProcessHandler(list<CharacterData>&);
        void normalizeAspect(vector<vector<int> >&);
        void affixWhiteRows(vector<vector<int> >&, int);
        void affixWhiteCols(vector<vector<int> >&, int);
        void flipImage(vector<vector<int> >&);
        // functions to find black distribution of an image
        vector<int> findHorDistribution(vector<vector<int> >, int);
        vector<int> findVerDistribution(vector<vector<int> >, int);
        int findHorThreshold(vector<vector<int> >);
        int findVerThreshold(vector<vector<int> >);
        int findNumChars(vector<vector<int> >&, double);
        int findNumLines(vector<vector<int> >&, int);
        // geometry functions
        int findYPos(vector<vector<int> >&);
        int findArea(vector<vector<int> >&, int);
        int meanArea(list<CharacterData>&);
        int sdArea(list<CharacterData>&);
        int meanWidth(list<CharacterData>&);
        int sdWidth(list<CharacterData>&);
        int meanHeight(list<CharacterData>&);
        int sdHeight(list<CharacterData>&);
        int getDistance(int, int);
        double findSlope(int*, int*);
        // for diagnostic purposes
        void printDist(vector<int>&);
        void printVector(vector<vector<int> >);
};

// variables
string infile;
list<CharacterData> tempList;
bool firstR = false;
bool firstSR = false;
bool kFlag = false;
bool train;
bool release;
int bigCharThreshold;
int meanW;

/******************************************************************
*
* Outputs, these are used for other modules
*
******************************************************************/

list<CharacterData> listChars; // list of chars
stringstream nsIndex; // NS-Index
stringstream sIndex; // S-Index
stringstream rIndex; // R-Index
stringstream srIndex; // SR-Index
char* nsArr;
char* sArr;
char* rArr;
char* srArr;

extern "C" {
    Segmenter* getSegmenterInstance(char* image) {
        return new Segmenter(string(image));
    }
    char* getNSIndex(Segmenter *instance) {
        string ns_index = instance->getNSIndex();
        int size = strlen(ns_index.c_str());
        nsArr = new char[size + 1];
        for (int i = 0; i < size; i++) {
            nsArr[i] = ns_index.c_str()[i];
        }
        nsArr[size] = '\0';
        return nsArr;
    }
    char* getSIndex(Segmenter *instance) {
        string s_index = instance->getSIndex();
        int size = strlen(s_index.c_str());
        sArr = new char[size + 1];
        for (int i = 0; i < size; i++) {
            sArr[i] = s_index.c_str()[i];
        }
        sArr[size] = '\0';
        return sArr;
    }
    char* getRIndex(Segmenter *instance) {
        string r_index = instance->getRIndex();
        int size = strlen(r_index.c_str());
        rArr = new char[size + 1];
        for (int i = 0; i < size; i++) {
            rArr[i] = r_index.c_str()[i];
        }
        rArr[size] = '\0';
        return rArr;
    }
    char* getSRIndex(Segmenter *instance) {
        string sr_index = instance->getSRIndex();
        int size = strlen(sr_index.c_str());
        srArr = new char[size + 1];
        for (int i = 0; i < size; i++) {
            srArr[i] = sr_index.c_str()[i];
        }
        srArr[size] = '\0';
        return srArr;
    }
    void destroySegmenterInstance(Segmenter* instance) {
        delete[] nsArr;
        delete[] sArr;
        delete[] rArr;
        delete[] srArr;
        delete instance;
    }
}