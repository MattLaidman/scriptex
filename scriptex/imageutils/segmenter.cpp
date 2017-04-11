#include "segmenter.h"

/******************************************************************
*
* Main Driver
*
******************************************************************/

/* effective main Driver
 *
 * @param img - file to segment */
Segmenter::Segmenter(string img) {
	writeMid = false;
	train = false; // flag for training; T is training mode
	release = true; // flag for release; T is release vers.
	vector<vector<int> > image = decodeImage(img); // infile
	segmentHandler(image); // segment handler call
	if (!train) { // if training mode on
		indexHandler(listChars); // do not do indices if training
	}
	postProcessHandler(listChars); // postprocess images
	if (!release) { // if release version, don't print diagnostic indices'
		cout << "NS: " << nsIndex.str() << endl;
		cout << "S: " << sIndex.str() << endl;
		cout << "R: " << rIndex.str() << endl;
		cout << "SR: " << srIndex.str() << endl;
	}
}

// returns ns-index to python driver
string Segmenter::getNSIndex() {
	return nsIndex.str();
}

// returns s-index to python driver
string Segmenter::getSIndex() {
	return sIndex.str();
}

// returns r-index to python driver
string Segmenter::getRIndex() {
	return rIndex.str();
}

// returns sr-index to python driver
string Segmenter::getSRIndex() {
	return srIndex.str();
}

/******************************************************************
*
* File I/O Functions
*
******************************************************************/

/* function to convert input image to usable array
 *
 * @param images - the string provided by decoder
 * @return the 2D vector of integers rep. the image */
vector<vector<int> > Segmenter::decodeImage(string images) {
	vector<string> tokens;
	istringstream iss(images);
	for (string images; iss >> images ; ) {
		tokens.push_back(images);
	}
	Decoder decoder(tokens, true);
	vector<vector<int> > decodedVector = decoder.getImage();
	flipImage(decodedVector);
	return decodedVector;
}

/* function to convert .txt input file
* to usable array.
*
* @param filename - the filename to read from
* @return a 2D integer vector of the image */
vector<vector<int> > Segmenter::fileToArray(string filename) {
	int dim[2] = { 0,0 }; // dimensions of the image
	int temp;
	ifstream imageFile(filename.c_str()); // open image .txt
	imageFile >> dim[0] >> dim[1]; // init dimensions
	// create a 2D integer vector of the required dimensions
	vector<vector<int> > img(dim[0], vector<int>(dim[1]));
	for (int i = 0; i < dim[1]; i++) {
		for (int j = 0; j < dim[0]; j++) {
			imageFile >> temp;
			img[j][i] = (temp > 127) ? 1 : 0; // direct mapping in grayscale
		}
	}
	imageFile.close(); // close the file/free memory
	return img; // return the vector
}

/* function to write .PGM intermediate files for diagnostic
* purposes. Creates a .pgm of every segmented character.
*
* @param input - the character to write .pgm for
* @param fileNum - the filename to save as (0..n) */
void Segmenter::writePGM(vector<vector<int> > &input, int ypos, int fileNum) {
	// make the directory to save to
	mkdir("./segmentPGM", 0700);
	stringstream filename;
	// filenames are 0..numChars
	filename << "./segmentPGM/" << fileNum << ".pgm";
	ofstream imageOutput(filename.str().c_str());
	imageOutput << "P2" << "\n"; // first header for .pgm
	// second header: dimensions of image
	imageOutput << input.size() << " " << input[0].size() << "\n";
	imageOutput << "1" << "\n"; // depth, third header
	for (unsigned int i = 0; i < input[0].size(); i++) {
		for (unsigned int j = 0; j < input.size(); j++) {
			if (writeMid && i > (unsigned int)ypos-5 && i < (unsigned int)ypos+5) {
				imageOutput << 0 << " ";
			} else {
				imageOutput << input[j][i] << " "; // insert pixel value
			}
		}
		imageOutput << "\n";
	}
	imageOutput.close();
}

/******************************************************************
*
* Segmentation Functions
*
******************************************************************/

/* segmentation handler, calls the function which
* begins the segmentation process.
*
* @param input - the image to segment */
void Segmenter::segmentHandler(vector<vector<int> > &input) {
	segmentIntoLines(input, 0, 0, 0); // start from SOF (row 0)
}

/* function to segment an image into individual lines.
* uses distribution of black-containing rows to find when
* lines begin and end, and creates a new vector for a line
*
* @param input - the image to be segmented 
* @param lineNum - the number of the line
* @param r = r-index of characters segmentable from line
* @param sr = sr-index of characters segmentable from line */
void Segmenter::segmentIntoLines(vector<vector<int> > &input, 
								unsigned int lineNum, unsigned int r, 
								unsigned int sr) {
	// theshold to ignore black pixels as noise
	int threshold = findVerThreshold(input);
	vector<int> verDist = findVerDistribution(input, threshold); // init dist
	unsigned int i, j = 0, k, l;
	while (j < input[0].size()) {
		// iterate until you find a row containing black
		for (i = j; verDist[i] <= threshold; i++);
		// iterate until you find a row containing no black
		for (j = i; verDist[j] > threshold; j++);
		if (j - i > (unsigned int)threshold) { // if tall enough
			vector<vector<int> > lineImage(input.size(), vector<int>(j - i));
			for (k = 0; k < j - i; k++) {
				for (l = 0; l < input.size(); l++) {
					lineImage[l][k] = input[l][k + i]; // init new image
				}
			}
			segmentIntoChars(lineImage, lineNum, r, sr); // segment this line into chars
			if (r == 0 && sr == 0) { // maintain line number only if R/SR = 1
				lineNum++; // inc line number
			}
		}
	}
}

/* function to segment a line into individual chars.
* uses distribution of black-containing rows to find when
* chars begin and end, and creates a new vector for a char
*
* @param input - the line to be segmented 
* @param lineNum - the line number a character was found on
* @param r - the r-index of segmented character
* @param sr - the sr-index of segmented character */
void Segmenter::segmentIntoChars(vector<vector<int> > &input, 
								unsigned int lineNum, unsigned int r, 
								unsigned int sr) {
	// theshold to ignore black pixels as noise
	int threshold = (sr == 0) ? findHorThreshold(input) : findPenWidth(input);
	threshold = (r == 0) ? threshold : 1;
	vector<int> horDist = findHorDistribution(input, threshold); // init dist
	unsigned int i, j = 0, k, l;
	while (j < input.size()) {
		// iteratre until you find a column containing black
		for (i = j; horDist[i] <= threshold && i < horDist.size(); i++);
		// iterate until you find a column containing no black
		for (j = i; horDist[j] > threshold && j < horDist.size(); j++);
		if (j - i > (unsigned int)threshold) { // if wide enough
			// new image for the segmented char
			vector<vector<int> > charImage(j - i, vector<int>(input[0].size()));
			for (k = 0; k < input[0].size(); k++) {
				for (l = 0; l < j - i; l++) {
					charImage[l][k] = input[l + i][k]; // init new image
				}
			}
			vector<vector<int> > tempVector = trimChars(charImage);
			int area = tempVector.size() * tempVector[0].size();
			// check for constituent lines in character (R > 0)
			if (!train && r == 0 && !tempList.empty() // if nonfirst element
			&& findNumLines(charImage, 1) > 1 // if constituent lines
			&& tempVector[0].size() > (meanHeight(tempList) * 2)) { // if sufficiently big
				firstR = true; // set so first R = 2
				segmentIntoLines(charImage, lineNum, 1, sr); // resegment
			// check for constituent characters in character (SR > 0)
			} else if (!train && sr == 0 && !tempList.empty() // if nonfirst element
			&& findNumChars(charImage, 10*threshold) > 1 // if constituent chars
			&& tempVector.size() > (meanWidth(tempList) * 1.75)) { // if sufficiently big
				firstSR = true; // so set first SR = 2
				segmentIntoChars(charImage, lineNum, r, 1); // resegment
			} else { // otherwise go as normal
				// append new character with characteristics to list
				int xP = floor((i + j)/2); // x-midpoint of char
				int yP = findYPos(charImage); // y-midpoint of char
				int he = tempVector[0].size(); // height of char
				int wi = tempVector.size(); // width of char
				int pos[2] = {xP, yP}; // position of character relative to line
				int rAdd = (firstR) ? 1 : 0; // is it start of R sequence?
				int srAdd = (firstSR) ? 1 : 0; // is it start of SR sequence?
				CharacterData newCharData; // empty CharacterData
				// then populate it with attributes
				newCharData.setPixels(charImage, pos, area, wi, he, lineNum, r+rAdd, sr+srAdd);
				tempList.push_back(newCharData); // append character to end of list
				firstR = false; // to ensure subsequent R is 1
				firstSR = false; // to ensure subsequent SR is 1
			}
		}
	}
	listChars.splice(listChars.end(), tempList); // splice temp list to main list
}

/******************************************************************
*
* Distribution Functions
*
******************************************************************/

/* function to find horizontal distribution of pixel
* values. Finds aggregate pixel value of all columns of
* pixels in the image.
*
* @param input - the image vector to find distribution on
* @param thresh - the threshold of noise
* @return 1D vector of column distributions */
vector<int> Segmenter::findHorDistribution(vector<vector<int> > input, int thresh) {
	vector<int> blackDist(input.size()); // init vector of app. size
	for (unsigned int hor = 0; hor < input.size(); hor++) {
		blackDist[hor] = 0; // initial value is zero
		for (unsigned int ver = 0; ver < input[0].size(); ver++) {
			// sum all pixels values but invert so 0 = 255, 255 = 0
			blackDist[hor] += abs((input[hor][ver]) - 1);
		}
		// set 0..1 instead of 0..n
		blackDist[hor] = (blackDist[hor] <= thresh) ? 0 : blackDist[hor];
	}
	return blackDist;
}

/* function to find vertical distribution of pixel
* values. Finds aggregate pixel value of all rows of
* pixels in the image.
*
* @param input - the image vector to find distribution on
* @param thresh - the threshold of noise
* @return 1D vector of row distributions */
vector<int> Segmenter::findVerDistribution(vector<vector<int> > input, int thresh) {
	vector<int> blackDist(input[0].size()); // init vector of app. size
	for (unsigned int ver = 0; ver < input[0].size(); ver++) {
		blackDist[ver] = 0; // initial value is zero
		for (unsigned int hor = 0; hor < input.size(); hor++) {
			// sum all pixel values but invert so 0 = 255, 255 = 0
			blackDist[ver] += abs((input[hor][ver]) - 1);
		}
		// set 0..1 instead of 0..n
		blackDist[ver] = (blackDist[ver] <= thresh) ? 0 : blackDist[ver];
	}
	return blackDist;
}

/* function to find the appropriate threshold to use
* checks the left 1% of cols and sees how much
* noise is present. Find the average amount of noise in a col
* and set that to horizontal noise threshold.
*
* @param input - the image vector to find threshold upon
* @return integer value representing the noise threshold */
int Segmenter::findHorThreshold(vector<vector<int> > input) {
	// use sample of rows = to 1% of image height
	int firstRows = (int)ceil(input.size()*0.01);
	// iterator: counts noisy pixels
	int counter = 0;
	for (int i = 0; i < firstRows; i++) {
		for (unsigned int j = 0; j < input[0].size(); j++) {
			// if noise
			if (input[i][j] == 0) {
				counter++; // inc counter
			}
		}
	}
	// return the mean occurrance of noisy pixels + 1
	return ceil(counter / firstRows) + 1;
}

/* function to find the appropriate threshold to use
* checks the top 1% of rows and sees how much
* noise is present. Find the average amount of noise in a row
* and set that to vertical noise threshold.
*
* @param input - the image vector to find threshold upon
* @return integer value representing the noise threshold */
int Segmenter::findVerThreshold(vector<vector<int> > input) {
	// use sample or columns = to 1% of image width
	int firstCols = (int)ceil(input[0].size()*0.01);
	// iterator: counts noisy pixels
	int counter = 0;
	for (int i = 0; i < firstCols; i++) {
		for (unsigned int j = 0; j < input.size(); j++) {
			// if noise
			if (input[j][i] == 0) {
				counter++; // inc counter
			}
		}
	}
	// return the mean occurrance of noisy pixels + 1
	return ceil(counter / firstCols) + 1;
}

/* function to find the number of characters within
 * a line.
 *
 * @param input - the line to check against
 * @param thresh - the noise threshold to use
 * @return the number of characters */
int Segmenter::findNumChars(vector<vector<int> > &input, double thresh) {
	vector<int> horDist = findHorDistribution(input, thresh);
	unsigned int i, j = 0;
	int numChars = 0;
	while (j < input.size()) {
		for (i = j; horDist[i] <= thresh && i < horDist.size(); i++);// find start of char
		for (j = i; horDist[j] > thresh && j < horDist.size(); j++); // find end of char
		if (j - i > 0.2*(unsigned int)thresh) { // if sufficiently big
			numChars++; // inc counter
		}
	}
	return numChars;
}

/* function to find the number of lines in an image
 *
 * @param input - the image to check against
 * @param thresh - the noise threshold to use
 * @return the number of lines */
int Segmenter::findNumLines(vector<vector<int> > &input, int thresh) {
	vector<int> verDist = findVerDistribution(input, thresh);
	unsigned int i, j = 0;
	int numLines = 0;
	while (j < input[0].size()) {
		for (i = j; verDist[i] <= thresh && i < verDist.size(); i++); // find start of line
		for (j = i; verDist[j] > thresh && j < verDist.size(); j++); // find end of line
		if (j - i > 2*(unsigned int)thresh) { // if sufficiently big
			numLines++; // inc counter
		}
	}
	return numLines;
}

/* function to find an approximate pen stroke width.
 * this metric is useful as it allows for easy segmentation
 * of square roots. 
 *
 * @param input - the character to find pen width on
 * @return the pen width */
int Segmenter::findPenWidth(vector<vector<int> > &input) {
	vector<int> horDist = findHorDistribution(input, 0);
	int highestMinimum = 0;
	/* check the last few columns of the image and
	 * sum the inked pixel frequency: the mean of this
	 * is assumed to be the pen stroke width */
	for (unsigned int j = 0; j < 5; j++) {
		highestMinimum = max(highestMinimum, horDist[(horDist.size() - j)-1]);
	}
	/* this value is:
	 * not 1, minor variance in pen width may screw it up
	 * not 2, as it will screw up minuses, equals, etc
	 * 1.5 as it is between these two */
	return ceil(highestMinimum*1.5);
}

/******************************************************************
*
* Post-Processing Functions
*
******************************************************************/

/* handler for postprocessing functions
 *
 * @param inList - the list of characters to process */
void Segmenter::postProcessHandler(list<CharacterData> &inList) {
	int j = 0;
	for (auto i : inList) { // foreach
		// if potential SR, remove top line
		if (i.getSR() == 1 && findNumLines(i.getPix(), 0) > 1) {
			removeTopLine(i.getPix());
		}
		normalizeAspect(i.getPix()); // set to 1:1 aspect (square)
		writePGM(i.getPix(), i.getPos()[1], j); // write PGM
		j++;
	}
	inList.clear(); // remove list
}

/* function to "normalize" a character image. Set the aspect
* ratio to 1:1 or square. Mutates input
*
* @param input - the character vector to normalize */
void Segmenter::normalizeAspect(vector<vector<int> > &input) {
	if (input.size() > input[0].size()) {
		// if white rows need to be added to become square
		affixWhiteRows(input, (input.size() - input[0].size()));
	}
	else if (input[0].size() > input.size()) {
		// if white columns need to be added to become square
		affixWhiteCols(input, (input[0].size() - input.size()));
	}
	/* it is possible for neither of the above to return true
	* in this case do nothing as the character is already square */
}

/* function to append/prepend white rows to an image to become square
* mutates input
*
* @param input - the character vector to affix to
* @param dimDiff - the difference of dimensions */
void Segmenter::affixWhiteRows(vector<vector<int> > &input, int dimDiff) {
	int backgroundValue = 1;
	// create new vector of desired dimensions
	vector<vector<int> > temp(input.size(), vector<int>(input[0].size() + dimDiff));
	for (unsigned int i = 0; i < temp[0].size(); i++) {
		for (unsigned int j = 0; j < temp.size(); j++) {
			if (i < (unsigned int)dimDiff / 2) { // if upper affixed white row
				temp[j][i] = backgroundValue;
			}
			else if (i < input[0].size() + (int)dimDiff / 2) { // leave be
				temp[j][i] = input[j][i - (int)dimDiff / 2];
			}
			else { // if bottom affixed white row
				temp[j][i] = backgroundValue;
			}
		}
	}
	input = temp; // mutate
}

/* function to append/prepend white columns to an image to become square
* mutates input
*
* @param input - the character vector to affix to
* @param dimDiff - the difference of dimensions */
void Segmenter::affixWhiteCols(vector<vector<int> > &input, int dimDiff) {
	int backgroundValue = 1;
	// create new vector of desired dimensions
	vector<vector<int> > temp(input.size() + dimDiff, vector<int>(input[0].size()));
	for (unsigned int i = 0; i < temp[0].size(); i++) {
		for (unsigned int j = 0; j < temp.size(); j++) {
			if (j < (unsigned int)dimDiff / 2) { // if left affixed white col
				temp[j][i] = backgroundValue;
			}
			else if (j < input.size() + (int)dimDiff / 2) { // leave be
				temp[j][i] = input[j - (int)dimDiff / 2][i];
			}
			else { // if right affixed white col
				temp[j][i] = backgroundValue;
			}
		}
	}
	input = temp; // mutate
}

/* function to flip input image to appropriate "look"
 * input from decoder is mirrored along the diagonal axis
 * and needs to be set to normal before it can be segmented
 * Function mutates input
 *
 * @param input - the image to flip */
void Segmenter::flipImage(vector<vector<int> > &input) {
	// create temp vector with rows = cols of input
	vector<vector<int> > temp(input[0].size(), vector<int>(input.size()));
	for (unsigned int i = 0; i < input[0].size(); i++) {
		for (unsigned int j = 0; j < input.size(); j++) {
			temp[i][j] = input[j][i]; // make rows -> cols and viceversa
		}
	}
	input = temp; // mutate
}

/* function to remove the top bar from square rooted
 * characters. The top bar kills recognition, so it must
 * be removed. Mutates input
 *
 * @param input - the character to remove top line on */
void Segmenter::removeTopLine(vector<vector<int> > &input) {
	vector<int> verDist = findVerDistribution(input, 0);
	unsigned int i = 0;
	// find point where black pixels begins
	for (; verDist[i] == 0 && i < verDist.size(); i++);
	// find point where black pixels end
	for (; verDist[i] > 0 && i < verDist.size(); i++) {
		for (unsigned int j = 0; j < input.size(); j++) {
			input[j][i] = 1; // make them white
		}
	}
}

/* function to find absolute closest dimensions to black
 * pixels in a character. Equivalent to an earlier function which
 * trimmed characters.
 *
 * @param input - the character to find area, height, etc on
 * @return a vector with as close to pixels as possible */
vector<vector<int> > Segmenter::trimChars(vector<vector<int> > input) {
	vector<int> verDist = findVerDistribution(input, 0);
	int actualHeight = verDist.size(); // find initial height
	unsigned int i = 0, j = verDist.size()-1;
	/* iterate over distribution to find a row with inked
	 * pixels, decreasing height as you go */
	for (; verDist[i] == 0; i++, actualHeight--);
	// same as above but start from bottom
	for (; verDist[j] == 0; j--, actualHeight--);
	// make a temporary vector to return
	vector<vector<int> > temp(input.size(), vector<int>(actualHeight));
	for (unsigned int k = 0; k < temp[0].size(); k++) {
		for (unsigned int l = 0; l < temp.size(); l++) {
			temp[l][k] = input[l][i+k]; // init new vector
		}
	}
	return temp; // does not mutate input
}

/******************************************************************
*
* Index Generation Functions
*
******************************************************************/

/* index generation handler, finds the formatting indices
 * for each character
 *
 * @param inList - the list of segmented character */
void Segmenter::indexHandler(list<CharacterData> &inList) {
	// i = element n, j = element n-1
	int c = 0; // counter
	CharacterData j, k; // k is anchor character
	// init threshold for scripts (big characters)
	bigCharThreshold = meanHeight(listChars);
	// init mean width global var
	meanW = meanWidth(inList);
	/* I do the above because these values are needed in
	 * multiple frames and the value will be static each call. Why
	 * resolve the function n times if I only need it once?
	 * Overall, it improves performance by around 17% */
	for (auto i : inList) { // foreach
		createRIndex(i); // get R-Index of n
		createSRIndex(i); // get SR-Index of n
		if (c > 0) {  // if not first element
			createNSIndex(i, j);  // get NS-Index of n compared to n-1
			createSIndex(i, j, k); // get S-Index of n compared to n-1
			// if anchor not set and anchor should be set
			if (kFlag == false
			&& i.getS() != j.getS() 
			&& j.getS() == 0) {
				k = j; // set anchor to n-1
				kFlag = true; // anchoring enabled
			}
		} else { // otherwise assume 1st element
			nsIndex << "1 "; // n = 0 is NS = 1
			sIndex << "0 "; // n = 0 is S = 0
		}
		j = i; // get new n-1
		c++; // inc counter
	}
}

/* function to create NS-Index over all characters
 *
 * @param ina - character n
 * @param inb - characer n-1 */
void Segmenter::createNSIndex(CharacterData &ina, CharacterData &inb) {
	if (ina.getLine() != inb.getLine()) {
		nsIndex << "-1 "; // if new line, make newline
	} else if (getDistance(ina.getPos()[0], inb.getPos()[0]) > 2*meanW) {
		nsIndex << "0 "; // if distance is high, make space
	}
	nsIndex << "1 "; // make character
}

/* function to create R-Index over all characters
 *
 * @param input - the character to find R on */
void Segmenter::createRIndex(CharacterData &input) {
	rIndex << input.getR() << " "; // trait found earlier, just append it
}

/* function to create SR-Index over all characters
 *
 * @param input - the character to find SR on */
void Segmenter::createSRIndex(CharacterData &input) {
	srIndex << input.getSR() << " "; // trait found earlier, just append it
}

/* function to create S-Index over all characters
 *
 * @param a - character n
 * @param b - character n-1
 * @param k - anchor character k */
void Segmenter::createSIndex(CharacterData &a, CharacterData &b, CharacterData &k) {
	int lowerA[2] = {a.getPos()[0], a.getPos()[1]+a.getHeight()/2};
	//int lowerB[2] = {b.getPos()[0], b.getPos()[1]+b.getHeight()/2};
	int lowerK[2] = {k.getPos()[0], k.getPos()[1]+k.getHeight()/2};
	//double lowermn = round(1000*findSlope(lowerA, lowerB))/1000;
	double lowermk = round(1000*findSlope(lowerA, lowerK))/1000;
	// slope between n and n-1
	double mn = round(1000*findSlope(a.getPos(), b.getPos()))/1000;
	// slope between n and k
	double mk = round(1000*findSlope(a.getPos(), k.getPos()))/1000;
	/* if entering an R or SR, or char n is too big, or in
	 * chain but it needs to be broken, break chain */
	if (b.getR() == a.getR() && b.getSR() == a.getSR()
	&& a.getHeight() < bigCharThreshold && a.getPos()[0] > b.getPos()[0]
	&& !(kFlag && (abs(mk) < 0.4 && abs(lowermk) < 0.4))) {
		if (abs(mn) > 0.4) { // if slope (n,n-1) is big enough
			if (mn <= 0) { // if negative
				a.setS(b.getS() + 1); // its a superscript
			} else if (mn > 0) { // if positive
				a.setS(b.getS() - 1); // its a subscript
			} else {
				a.setS(b.getS());
			}
		} else { // otherwise
			a.setS(b.getS()); // keep chain going
		}
	} else { // if entering R/SR or character not big enough or chain stopping
		a.setS(0); // reset chain
		kFlag = false; // disable anchoring
	}
	sIndex << a.getS() << " "; // append degree to index
}

/******************************************************************
*
* Geometry Functions
*
******************************************************************/

/* function to find the weighted y-center of a character
 *
 * @param in - the character to find for
 * @return the y-center */
int Segmenter::findYPos(vector<vector<int> > &in) {
	/* as the distribution of inked pixels is a discrete sequence
	 * we can find the area under this curve by summing
	 * the frequency of inked pixels (y-axis of the distribution graph) */
	vector<int> verDist = findVerDistribution(in, 0);
	int sum = 0; // for summation
	unsigned int j = 0; // the tentative y-center
	for (int i : verDist) {
		sum += i; // add up the distribution values
	}
	/* if you then find half of the area, you can
	 * find the x-value at which you reach half. this
	 * constitutes the weighted middle */
	sum /= 2;
	// subtract from half of sum until you hit zero
	for (; sum > 0; j++) {
		sum -= verDist[j];
	}
	/* at this point you have the weighted midpoint, or the midpoint
	 * along a character's height with consideration for the density
	 * of pixels at a certain height */
	return j;
}

/* function to find the slope of the lineImage
 * between two characters
 *
 * @param a - first character
 * @param b - second character
 * @return the slope */
double Segmenter::findSlope(int *a, int *b) {
	return (double)(b[1] - a[1])/(b[0] - a[0]);
}

/* functions to find distance between two chars
 *
 * @param x1 - x-pos of first char
 * @param x2 - x-pos of second char
 * @return the distance */
int Segmenter::getDistance(int x1, int x2) {
	return abs(x2 - x1); // horizontal constituent of ManH.metric
}

/* function to find the mean area of characters
 *
 * @param inList - the list of characters to find mean on
 * @return the mean area */
unsigned int Segmenter::meanArea(list<CharacterData> &inList) {
	unsigned long long int totalArea = 0;
	for (auto i : inList) { // foreach
		totalArea += i.getArea(); // sum area
	}
	return floor(totalArea/inList.size()); // find average
}

/* function to find the standard deviation of area
 *
 * @param inList - the list of characters to find SD on
 * @return the standard deviation */
unsigned int Segmenter::sdArea(list<CharacterData> &inList) {
	int mean = meanArea(inList); // need mean
	unsigned long long int totalSubvariance = 0; // total subvariance
	for (auto i : inList) { // foreach
		totalSubvariance += pow(i.getArea() - mean, 2); // sum subvariance
	}
	unsigned int variance = floor(totalSubvariance / inList.size()); // find variance
	return floor(pow(variance, 0.5)); // find SD, return it
}

/* function to find the mean width of characters
 *
 * @param inList - the list of characters to find mean width
 * @return the mean width */
unsigned int Segmenter::meanWidth(list<CharacterData> &inList) {
	unsigned long long int totalWidth = 0;
	for (auto i : inList) { // foreach
		totalWidth += i.getWidth(); // sum widths
	}
	return floor(totalWidth/inList.size()); // find average
}

/* function to find the standard deviation of widths
 *
 * @param inList - the list of chars to find SD width on
 * @return the SD */
unsigned int Segmenter::sdWidth(list<CharacterData> &inList) {
	int mean = meanWidth(inList); // find mean width
	unsigned long long int totalSubvariance = 0; // total subvariance
	for (auto i : inList) { // foreach
		totalSubvariance += pow(i.getWidth() - mean, 2); // sum subvariance
	}
	unsigned int variance = floor(totalSubvariance / inList.size()); // find variance
	return floor(pow(variance, 0.5)); // find SD, return it
}

/* function to find the mean height of characters
 *
 * @param inList - the list of characters to find mean height
 * @return the mean height */
unsigned int Segmenter::meanHeight(list<CharacterData> &inList) {
	unsigned long long int totalHeight = 0;
	for (auto i : inList) { // foreach
		totalHeight += i.getHeight(); // sum widths
	}
	return floor(totalHeight/inList.size()); // find average
}

/* function to find the standard deviation of heights
 *
 * @param inList - the list of chars to find SD height on
 * @return the SD */
unsigned int Segmenter::sdHeight(list<CharacterData> &inList) {
	int mean = meanHeight(inList); // find mean width
	unsigned long long int totalSubvariance = 0; // total subvariance
	for (auto i : inList) { // foreach
		totalSubvariance += pow(i.getHeight() - mean, 2); // sum subvariance
	}
	unsigned int variance = floor(totalSubvariance / inList.size()); // find variance
	return floor(pow(variance, 0.5)); // find SD, return it
}

/******************************************************************
*
* Diagnostic Functions
*
******************************************************************/

/* diagnostic tool for development, print an image's distribution
*
* @param dist - the distribution to print */
void Segmenter::printDist(vector<int> &dist) {
	for (unsigned int i = 0; i < dist.size(); i++) {
		cout << dist[i] << " ";
	}
}

/* diagnostic tool for development, print an image vector
*
* @param input - the image vector to print */
void Segmenter::printVector(vector<vector<int> > input) {
	for (unsigned int i = 0; i < input[0].size(); i++) {
		for (unsigned int j = 0; j < input.size(); j++) {
			cout << input[j][i] << " ";
		}
		cout << "\n";
	}
	cout << "\n";
}