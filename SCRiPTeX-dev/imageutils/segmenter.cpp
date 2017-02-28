#include "segmenter.h"

Segmenter::Segmenter(string img) {
	statusUpdates = false; // flag for diagnostic purposes
	time_t now = time(0); // timing algorithm
	vector<vector<int>> image = decode(img); // infile
	segment(image); // segment handler call

	/*************************************
	* Character Position Index for Tex.Ass
	* Queue of segmented characters is listChars
	**************************************/
	characterIndex = genIndex(listSpaces); // <--------------
	
	//writeToFile(listChars, outfile1); // not needed for final
	time_t after = time(0);
	if (statusUpdates) {
		cout << "Process takes " << (after - now) << " seconds." << endl;
	}
}

string Segmenter::getIndex() {
	return characterIndex;
}

/******************************************************************
*
* Segmentation Functions
*
******************************************************************/

/* Decodes the image
*
* @param input - the path to the image as a string */
vector<vector<int>> Segmenter::decode(string image) {
	Decoder decoder(image, true);
	return decoder.getImage();
}

/* segmentation handler, calls the function which
* begins the segmentation process.
*
* @param input - the image to segment */
void Segmenter::segment(vector<vector<int>> input) {
	segmentIntoLines(input); // start from SOF (row 0)
	listSpaces.push('e'); // push EoF flag to index
}

/* function to segment a line into individual chars.
* uses distribution of black-containing rows to find when
* chars begin and end, and creates a new vector for a char
*
* @param input - the line to be segmented */
void Segmenter::segmentIntoChars(vector<vector<int>> input) {
	// theshold to ignore black pixels as noise
	int threshold = findHorThreshold(bwify(input));
	vector<int> horDist = findHorDistribution(bwify(input), threshold); // init dist
	unsigned int i, j = 0, charWidth;
	while (true) {
		if (j >= input.size()) { // if there are more characters
			break;
		}
		// iteratre until you find a column containing black
		for (i = j; i < horDist.size(); i++) {
			if (horDist[i] == 1) { break; } // i is start point
		}
		// iterate until you find a column containing no black
		for (j = i; j < horDist.size(); j++) {
			if (horDist[j] == 0) { break; } // j is end point
		}
		charWidth = j - i; // the width of the character
		if (charWidth != 0) { // this denotes end of algorithm if j-i = 0
			if (charWidth >(unsigned int)(threshold*5)) {
				// new image for the segmented char
				vector<vector<int>> charImage(charWidth, vector<int>(input[0].size()));
				for (unsigned int k = 0; k < input[0].size(); k++) {
					for (unsigned int l = 0; l < charWidth; l++) {
						charImage[l][k] = input[l + i][k]; // init new image
					}
				}
				normalizeAspect(charImage); // set to 1:1 aspect (square)
				writePGM(charImage);
				listChars.push(charImage); // append character to end of queue
			}
		}
	}
}

/* function to segment an image into individual lines.
* uses distribution of black-containing rows to find when
* lines begin and end, and creates a new vector for a line
*
* @param input - the image to be segmented */
void Segmenter::segmentIntoLines(vector<vector<int>> input) {
	// theshold to ignore black pixels as noise
	int threshold = findVerThreshold(bwify(input));
	vector<int> verDist = findVerDistribution(bwify(input), threshold); // init dist
	unsigned int i, j = 0;
	while (true) {
		if (j >= input[0].size()) { // if there are more lines
			break;
		}
		// iterate until you find a row containing black
		for (i = j; i < verDist.size(); i++) {
			if (verDist[i] == 1) { break; } // i is start point
		}
		// iterate until you find a row containing no black
		for (j = i; j < verDist.size(); j++) {
			if (verDist[j] == 0) { break; } // j is end point
		}
		unsigned int lineHeight = j - i; // the height of the line
		if (lineHeight != 0) { // this denotes end of algorithm if j-i = 0
			if (lineHeight >(unsigned int)(threshold*5)) { // if viable line
												// new image for the segmented line
				vector<vector<int>> lineImage(input.size(), vector<int>(lineHeight));
				for (unsigned int k = 0; k < lineHeight; k++) {
					for (unsigned int l = 0; l < input.size(); l++) {
						lineImage[l][k] = input[l][k + i]; // init new image
					}
				}
				findCharIndex(lineImage, threshold); // find position of chars/spaces
				segmentIntoChars(lineImage); // segment this line into chars
			}
		}
	}
}

/* function to find the appropriate threshold to use
* checks the left 1% of cols and sees how much
* noise is present. Find the average amount of noise in a col
* and set that to horizontal noise threshold.
*
* @param input - the image vector to find threshold upon
* @return integer value representing the noise threshold
*/
int Segmenter::findHorThreshold(vector<vector<int>> input) {
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
	return (int)ceil(counter / firstRows) + 1;
}

/* function to find the appropriate threshold to usevector<vector<int>>
* checks the top 1% of rows and sees how much
* noise is present. Find the average amount of noise in a row
* and set that to vertical noise threshold.
*
* @param input - the image vector to find threshold upon
* @return integer value representing the noise threshold
*/
int Segmenter::findVerThreshold(vector<vector<int>> input) {
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
	return (int)ceil(counter / firstCols) + 1;
}

/* function to create a B+W copy of an image to find
 * distributions upon. 
 *
 * @param input - the image to B+Wify
 * @return a black and white copy of input */
vector<vector<int>> Segmenter::bwify(vector<vector<int>> input) {
	vector<vector<int>> bwCopy(input.size(), vector<int>(input[0].size()));
	for (unsigned int i = 0; i < input.size(); i++) {
		for (unsigned int j = 0; j < input[0].size(); j++) {
			// copy is 0..1 instead of 0..255
			bwCopy[i][j] = (input[i][j] > 127) ? 1 : 0;
		}
	}
	return bwCopy;
}

/* function to find horizontal distribution of pixel
* values. Finds aggregate pixel value of all columns of
* pixels in the image.
*
* @param input - the image vector to find distribution on
* @param thresh - the threshold of noise
* @return 1D vector of column distributions */
vector<int> Segmenter::findHorDistribution(vector<vector<int>> input, int thresh) {
	vector<int> blackDist(input.size()); // init vector of app. size
	for (unsigned int hor = 0; hor < input.size(); hor++) {
		blackDist[hor] = 0; // initial value is zero
		for (unsigned int ver = 0; ver < input[0].size(); ver++) {
			// sum all pixels values but invert so 0 = 255, 255 = 0
			blackDist[hor] += abs((input[hor][ver]) - 1);
		}
		// set 0..1 instead of 0..n
		blackDist[hor] = (blackDist[hor] < thresh) ? 0 : 1;
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
vector<int> Segmenter::findVerDistribution(vector<vector<int>> input, int thresh) {
	vector<int> blackDist(input[0].size()); // init vector of app. size
	for (unsigned int ver = 0; ver < input[0].size(); ver++) {
		blackDist[ver] = 0; // initial value is zero
		for (unsigned int hor = 0; hor < input.size(); hor++) {
			// sum all pixel values but invert so 0 = 255, 255 = 0
			blackDist[ver] += abs((input[hor][ver]) - 1);
		}
		// set 0..1 instead of 0..n
		blackDist[ver] = (blackDist[ver] < thresh) ? 0 : 1;
	}
	return blackDist;
}

/******************************************************************
*
* Post-Processing Functions
*
******************************************************************/

/* function to "normalize" a character image. Set the aspect
* ratio to 1:1 or square. Mutates input
*
* @param input - the character vector to normalize */
void Segmenter::normalizeAspect(vector<vector<int>> &input) {
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
void Segmenter::affixWhiteRows(vector<vector<int>> &input, int dimDiff) {
	int backgroundValue = findBackgroundColor(input);
	// create new vector of desired dimensions
	vector<vector<int>> temp(input.size(), vector<int>(input[0].size() + dimDiff));
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
void Segmenter::affixWhiteCols(vector<vector<int>> &input, int dimDiff) {
	int backgroundValue = findBackgroundColor(input);
	// create new vector of desired dimensions
	vector<vector<int>> temp(input.size() + dimDiff, vector<int>(input[0].size()));
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

/* function to determine appropriate background color
* to set for padding cols/rows for non-square character
* checks the corners to see which is the highest value (most
* likely to be background)
*
* @param input - the character to scan for bg color
* @return the grayscale value for the background */
int Segmenter::findBackgroundColor(vector<vector<int>> &input) {
	// check top corners
	int t = max(input[0][0], input[input.size() - 1][0]);
	// check bottome corners
	int b = max(input[0][input[0].size() - 1], input[input.size() - 1][input[0].size() - 1]);
	// return the highest value
	return max(t, b);
}

/******************************************************************
*
* Index Generation Functions
*
******************************************************************/

/* function to find the average character width in a line
*
* @param input - the line to inspect
* @return the average character width */
int Segmenter::findAvgCharWidth(vector<vector<int>> &input, int thresh) {
	// threshold to ignore chars
	vector<int> horDist = findHorDistribution(bwify(input), thresh);
	unsigned int i, j, start = 0;
	int numChars = 0;
	double avgCharWidth = 0.00;
	while (start < input.size()) {
		for (i = start; i < horDist.size(); i++) {
			if (horDist[i] == 1) { break; } // find start of char
		}
		for (j = i; j < horDist.size(); j++) {
			if (horDist[j] == 0) { break; } // find end of char
		}
		if (j - i >(unsigned int)thresh) { // if within reasonable width
			avgCharWidth += j - i; // sum char widths
			numChars++; // inc. number of characters
		}
		start = j; // for repetition
	}
	avgCharWidth /= numChars; // find avg
	return (int)avgCharWidth;
}

/* function to find the position of characters, spaces,
* and newlines.
*
* @param input - the line to find positions on */
void Segmenter::findCharIndex(vector<vector<int>> &input, int thresh) {
	int avgCharWidth = findAvgCharWidth(input, thresh);
	// spaces are avgCharWidth - (avgCharWidth *0.2) .. infinity
	unsigned int range = (unsigned int)(avgCharWidth*0.02);
	vector<int> horDist = findHorDistribution(bwify(input), thresh);
	unsigned int i, j, k, start = 0;
	while (start < input.size()) {
		for (i = start; i < horDist.size(); i++) {
			if (horDist[i] == 1) { break; } // find start of char
		}
		for (j = i; j < horDist.size(); j++) {
			if (horDist[j] == 0) { break; } // find end of char
		}
		if (j - i >(unsigned int)thresh) {
			listSpaces.push('c'); // append char to queue
		}
		for (k = j; k < horDist.size(); k++) {
			// k measures gap between characters
			if (horDist[k] == 1) {
				break;
			}
		}
		// if gap is big enough, it is a space
		if (k - j > avgCharWidth - range) {
			listSpaces.push('s'); // append space to queue
		}
		start = k;
	}
	listSpaces.push('n'); // end of line denotes newline
}

/* function to generate character index string
*
* @param inList - a queue of posiitons
* @return a string of character index */
string Segmenter::genIndex(queue<char> inList) {
	int counter = 0; // counter
    stringstream characterIndex;
    while (inList.front() != 'e') { // while queue top is not EOF
        if (inList.front() == 's') { // if space
            inList.pop();
        }
        else if (inList.front() == 'n') { // if newline
            characterIndex << "-1, ";
            inList.pop();
        }
        else if (inList.front() == 'c') { // if character
                                          // find number of successive 'c' in queue
            while (inList.front() == 'c') {
                counter++; // inc counter
                inList.pop();
            }
            characterIndex << counter << ", ";
            counter = 0;
        }
    }
    string returnString = characterIndex.str();
    return returnString;
}

/******************************************************************
*
* File I/O Functions
*
******************************************************************/

/* function to convert .txt input file
* to usable array.
*
* @param filename - the filename to read from
* @return a 2D integer vector of the image */
vector<vector<int>> Segmenter::fileToArray(string filename) {
	if (statusUpdates) {
		cout << "Reading " << filename.c_str() << " ... ";
	}
	int dim[2] = { 0,0 }; // dimensions of the image
	ifstream imageFile(filename.c_str()); // open image .txt
	imageFile >> dim[0] >> dim[1]; // init dimensions
								   // create a 2D integer vector of the required dimensions
	vector<vector<int>> img(dim[0], vector<int>(dim[1]));
	for (int i = 0; i < dim[1]; i++) {
		for (int j = 0; j < dim[0]; j++) {
			imageFile >> img[j][i]; // direct mapping in grayscale
		}
	}
	imageFile.close(); // close the file/free memory
	if (statusUpdates) {
		cout << "done!" << endl;
	}
	return img; // return the vector
}

/* function to write .PGM intermediate files for diagnostic
* purposes. Creates a .pgm of every segmented character.
*
* @param input - the character to write .pgm for */
void Segmenter::writePGM(vector<vector<int>> &input) {
	if (statusUpdates) {
		cout << "Writing " << listChars.size() << ".pgm ... ";
	}
	// make the directory to save to
	mkdir("./segmentPGM", 0700);
	stringstream filename;
	// filenames are 0..numChars
	filename << "./segmentPGM/" << listChars.size() << ".pgm";
	ofstream imageOutput(filename.str().c_str());
	imageOutput << "P2" << "\n"; // first header for .pgm
								 // second header: dimensions of image
	imageOutput << input[0].size() << " " << input.size() << "\n";
	imageOutput << "255" << "\n"; // depth, third header
	for (unsigned int i = 0; i < input[0].size(); i++) {
		for (unsigned int j = 0; j < input.size(); j++) {
			imageOutput << input[j][i] << " "; // insert pixel value
		}
		imageOutput << "\n";
	}
	imageOutput.close();
	if (statusUpdates) {
		cout << "done!" << endl;
	}
}

/******************************************************************
*
* Deprecated Functions (Prototype File I/O)
*
******************************************************************/

/* function to write each character vector to a file
* vectors are flattened to 1D with dimensions prepending the characters
*
* @param input - a list of 2D vectors representing characters
* @param filename - the filename to write to */
void Segmenter::writeToFile(queue<vector<vector<int>>> &inList, string filename) {
	if (statusUpdates) {
		cout << "Writing " << filename.c_str() << " ... ";
	}
	ofstream outFile;
	outFile.open(filename.c_str());
	outFile << inList.size() << "\n"; // append number of chars to file
	vector<vector<int>> temp; // temporary vector
	int maxChars = inList.size(); // number of chars in queue
	for (int i = 0; i < maxChars; i++) {
		temp = inList.front(); // access and init temp to first char
		inList.pop(); // can safely remove char from queue
		outFile << temp[0].size() << " "; // append height to file
		outFile << temp.size() << " "; // append width to file
		for (unsigned int j = 0; j < temp[0].size(); j++) {
			for (unsigned int k = 0; k < temp.size(); k++) {
				outFile << temp[k][j] << " "; // the pixel data of char
			}
		}
		outFile << "\n"; // newline for next character
	}
	outFile.close();
	if (statusUpdates) {
		cout << "done!" << endl;
	}
}

/* function to write to file the character index
*
* @param inList - a queue of posiitons
* @param filename - the filename to write to */
void Segmenter::writeIndex(queue<char> &inList, string filename) {
	int temp = 0;
	if (statusUpdates) {
		cout << "Writing " << filename.c_str() << " ... ";
	}
	ofstream outFile;
	outFile.open(filename.c_str());
	while (inList.front() != 'e') { // while queue top is not EOF
		if (inList.front() == 's') { // if space
			outFile << " "; // write space
			inList.pop();
		}
		else if (inList.front() == 'n') { // if newline
			outFile << "\n"; // write newline
			inList.pop();
		}
		else if (inList.front() == 'c') { // if character
										  // find number of successive 'c' in queue
			while (inList.front() == 'c') {
				temp++; // inc ocunter
				inList.pop();
			}
			outFile << temp; // write counter
			temp = 0;
		}
	}
	if (statusUpdates) {
		cout << "done!" << endl;
	}
	outFile.close();
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
void Segmenter::printVector(vector<vector<int>> &input) {
	for (unsigned int i = 0; i < input[0].size(); i++) {
		for (unsigned int j = 0; j < input.size(); j++) {
			cout << input[j][i] << " ";
		}
		cout << "\n";
	}
	cout << "\n";
}
