#include <iostream>
#include <stdio.h>
#include <fstream>
#include <vector>
#include <complex>
#include <queue>
#include <string>
#include <sstream>
#include <sys/stat.h>
#include <sys/types.h>

using namespace std;


typedef vector<vector<int> > pixelData;
typedef unsigned int usint;

// flags
bool makePGM;
bool statusUpdates;
bool grayscale;
bool trimChars;
// the threshold for noise
double threshPerc;
// queue of characters (FIFO)
queue<pixelData> listChars;
// queue of spaces (FIFO)
queue<char> listSpaces;
// filenames for I/O
string infile;
string outfile1;
string outfile2;


void _segmentImage(string, string, string);
extern "C" void segmentImage(char* infile, char* segmented, char* index) {
    _segmentImage(string(infile), string(segmented), string(index));
}

/* function to convert .txt input file
 * to usable array.
 *
 * @param filename - the filename to read from
 * @return a 2D integer vector of the image */
pixelData fileToArray(string);

/* segmentation handler, calls the function which
 * begins the segmentation process.
 *
 * @param input - the image to segment */
void segment(pixelData);

/* function to segment a line into individual chars.
 * uses distribution of black-containing rows to find when
 * chars begin and end, and creates a new vector for a char
 *
 * @param input - the line to be segmented
 * @param begin - the column to start processing */
void segmentIntoChars(pixelData&, int);

/* function to segment an image into individual lines.
 * uses distribution of black-containing rows to find when
 * lines begin and end, and creates a new vector for a line
 *
 * @param input - the image to be segmented
 * @param begin - the row to start processing */
void segmentIntoLines(pixelData&, int);

/* function to find the average character width in a line
 *
 * @param input - the line to inspect
 * @return the average character width */
int findAvgCharWidth(pixelData&);

/* function to find the position of characters, spaces,
 * and newlines.
 *
 * @param input - the line to find positions on */
void findCharIndex(pixelData&);

/* function to "normalize" a character image. Set the aspect
 * ratio to 1:1 or square. Mutates input
 *
 * @param input - the character vector to normalize */
void normalizeAspect(pixelData&);

/* function to append/prepend white rows to an image to become square
 * mutates input
 *
 * @param input - the character vector to affix to
 * @param dimDiff - the difference of dimensions */
void affixWhiteRows(pixelData&, int);

/* function to append/prepend white columns to an image to become square
 * mutates input
 *
 * @param input - the character vector to affix to
 * @param dimDiff - the difference of dimensions */
void affixWhiteCols(pixelData&, int);

/* function to remove whitespace from a character vector. Sometimes
 * you'll end up with white columns or rows on the extremes
 * of a character after segmentation: this algorithm removes these. 
 * Mutates input vector to be cropped as close to black pixels as possible
 *
 * @param input - the character vector to remove whitespace from */
void cullWhitespace(pixelData&);

/* function to find horizontal distribution of pixel
 * values. Finds aggregate pixel value of all columns of
 * pixels in the image.
 *
 * @param input - the image vector to find distribution on
 * @param thresh - the threshold of noise
 * @return 1D vector of column distributions */
vector<int> findHorDistribution(pixelData&, int);

/* function to find vertical distribution of pixel
 * values. Finds aggregate pixel value of all rows of
 * pixels in the image.
 *
 * @param input - the image vector to find distribution on
 * @param thresh - the threshold of noise
 * @return 1D vector of row distributions */
vector<int> findVerDistribution(pixelData&, int);
/* function to write each character vector to a file
 * vectors are flattened to 1D with dimensions prepending the characters
 *
 * @param input - a list of 2D vectors representing characters
 * @param filename - the filename to write to */
void writeToFile(queue<pixelData>&, string);

/* function to write .PGM intermediate files for diagnostic
 * purposes. Creates a .pgm of every segmented character.
 *
 * @param input - the character to write .pgm for */
void writePGM(pixelData&);

/* function to write to file the character index
 *
 * @param inList - a queue of posiitons
 * @param filename - the filename to write to */
void writeIndex(queue<char>&, string);
/* diagnostic tool for development, print an image's distribution
 *
 * @param dist - the distribution to print */
void printDist(vector<int>&);

/* diagnostic tool for development, print an image vector
 *
 * @param input - the image vector to print */
void printVector(pixelData&);