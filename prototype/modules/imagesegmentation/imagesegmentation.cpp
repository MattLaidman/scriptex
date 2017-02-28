#include "imagesegmentation.h"

void _segmentImage(string input, string segmented, string index) {
	infile = input;
	outfile1 = segmented;
	outfile2 = index;
	threshPerc = 0.5; // default 0.5%
	makePGM = false; // flag for writing PGM intermediates
	statusUpdates = false; // flag for diagnostic purposes
	grayscale = false; // is input image grayscale? If F, assume B+W
	trimChars = true; // trim characters to be as close to black as possible
	time_t now = time(0); // timing algorithm
	pixelData image = fileToArray(infile); // infile
	segment(image); // segment handler call
	writeToFile(listChars, segmented); // outfile1
	writeIndex(listSpaces, index); // outfile2
	time_t after = time(0);
	if (statusUpdates) {
		cout << "Process takes " << (after-now) << " seconds." << endl;
	}
}

/* function to convert .txt input file
 * to usable array.
 *
 * @param filename - the filename to read from
 * @return a 2D integer vector of the image */
pixelData fileToArray(string filename) {
	if (statusUpdates) {
		cout << "Reading " << filename.c_str() << " ... ";
	}
	int dim[2] = {0,0}; // dimensions of the image
	int temp; // temp for B+W insertion
	int maxWhite; // for grayscale check
	ifstream imageFile(filename.c_str()); // open image .txt
	imageFile >> dim[0] >> dim[1]; // init dimensions
	// create a 2D integer vector of the required dimensions
	pixelData img(dim[0], vector<int>(dim[1]));
	for (int i = 0; i < dim[1]; i++) {
		for (int j = 0; j < dim[0]; j++) {
			imageFile >> temp; // init as temp
			maxWhite = (grayscale) ? 128 : 1;
			if (temp < maxWhite) { 
				img[j][i] = 0; // set black
			} else { 
				img[j][i] = 1; // set white
			}
		}
	}
	imageFile.close();
	if (statusUpdates) {
		cout << "done!" << endl;
	}
	return img; // return the vector
}

/* segmentation handler, calls the function which
 * begins the segmentation process.
 *
 * @param input - the image to segment */
void segment(pixelData input) {
	segmentIntoLines(input, 0); // start from SOF (row 0)
	listSpaces.push('e'); // push EoF flag to index
}

/* function to segment a line into individual chars.
 * uses distribution of black-containing rows to find when
 * chars begin and end, and creates a new vector for a char
 *
 * @param input - the line to be segmented
 * @param begin - the column to start processing */
void segmentIntoChars(pixelData &input, int begin) {
	/* theshold to ignore black pixels as noise
	 * testing worked well at 0.4% and 0.5%; anything outside
	 * range causes errors in segmentation. */
	int threshold = (int)abs(((threshPerc/100) * input[0].size())+1);
	vector<int> horDist = findHorDistribution(input, threshold); // init dist
	usint i, j, charWidth;
	// iteratre until you find a column containing black
	for (i = begin; i < horDist.size(); i++) {
		if(horDist[i] == 1) { break; } // i is start point
	}
	// iterate until you find a column containing no black
	for (j = i; j < horDist.size(); j++) { 
		if(horDist[j] == 0) { break; } // j is end point
	}
	charWidth = j - i; // the width of the character
	if (charWidth != 0) { // this denotes end of algorithm if j-i = 0
		if (charWidth > threshold) {
			// new image for the segmented char
			pixelData charImage(charWidth, vector<int>(input[0].size()));
			for (usint k = 0; k < input[0].size(); k++) {
				for (usint l = 0; l < charWidth; l++) {
					charImage[l][k] = input[l+i][k]; // init new image
				}
			}
			if (trimChars) {
				cullWhitespace(charImage); // remove unnecessary rows of white
			}
			normalizeAspect(charImage); // set to 1:1 aspect (square)
			if (makePGM == true) {
				writePGM(charImage);
			}
			listChars.push(charImage); // append character to end of queue
		}
		if (j <= input.size()) { // recurse if there are more
			segmentIntoChars(input, j);
		}
	}
}

/* function to segment an image into individual lines.
 * uses distribution of black-containing rows to find when
 * lines begin and end, and creates a new vector for a line
 *
 * @param input - the image to be segmented
 * @param begin - the row to start processing */
void segmentIntoLines(pixelData &input, int begin) {
	/* theshold to ignore black pixels as noise
	 * testing worked well at 0.4% and 0.5%; anything outside
	 * range causes errors in segmentation. */
	int threshold = (int)abs(((threshPerc/100) * input.size())+1);
	vector<int> verDist = findVerDistribution(input, threshold); // init dist
	usint i, j, charWidth;
	// iterate until you find a row containing black
	for (i = begin; i < verDist.size(); i++) {
		if (verDist[i] == 1) { break; } // i is start point
	}
	// iterate until you find a row containing no black
	for (j = i; j < verDist.size(); j++) {
		if (verDist[j] == 0) { break; } // j is end point
	}
	usint lineHeight = j - i; // the height of the line
	if (lineHeight != 0) { // this denotes end of algorithm if j-i = 0
		if (lineHeight > (usint)threshold) { // if viable line
			// new image for the segmented line
			pixelData lineImage(input.size(), vector<int>(lineHeight));
			for (usint k = 0; k < lineHeight; k++) {
				for (usint l = 0; l < input.size(); l++) {
					lineImage[l][k] = input[l][k + i]; // init new image
				}
			}
			findCharIndex(lineImage); // find position of chars/spaces
			segmentIntoChars(lineImage, 0); // segment this line into chars
		}
		if (j <= input[0].size()) { // if there are more lines
			segmentIntoLines(input, j); // recurse if there are more
		}
	}
}

/* function to find the average character width in a line
 *
 * @param input - the line to inspect
 * @return the average character width */
int findAvgCharWidth(pixelData &input) {
	// threshold to ignore chars
	int thresh = (int)abs(((threshPerc/100) * input[0].size())+1);
	vector<int> horDist = findHorDistribution(input, thresh);
	usint i, j, start = 0;
	int numChars = 0;
	double avgCharWidth = 0.00;
	while(start < input.size()) {
		for (i = start; i < horDist.size(); i++) {
			if (horDist[i] == 1) { break; } // find start of char
		}
		for (j = i; j < horDist.size(); j++) {
			if (horDist[j] == 0) { break; } // find end of char
		}
		if (j - i > thresh) { // if within reasonable width
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
void findCharIndex(pixelData &input) {
	int avgCharWidth = findAvgCharWidth(input);
	// spaces are avgCharWidth - (avgCharWidth *0.2) .. infinity
	int range = (int)(avgCharWidth*0.02);
	int thresh = (int)abs(((threshPerc/100) * input[0].size())+1);
	vector<int> horDist = findHorDistribution(input, thresh);
	usint i, j, k, start = 0;
	while(start < input.size()) {
		for (i = start; i < horDist.size(); i++) {
			if (horDist[i] == 1) { break; } // find start of char
		}
		for (j = i; j < horDist.size(); j++) {
			if (horDist[j] == 0) { break; } // find end of char
		}
		if (j - i > thresh) {
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

/* function to "normalize" a character image. Set the aspect
 * ratio to 1:1 or square. Mutates input
 *
 * @param input - the character vector to normalize */
void normalizeAspect(pixelData &input) {
	if (input.size() > input[0].size()) {
		// if white rows need to be added to become square
		affixWhiteRows(input, (input.size()-input[0].size()));
	} else if (input[0].size() > input.size()) {
		// if white columns need to be added to become square
		affixWhiteCols(input, (input[0].size()-input.size()));
	}
	/* it is possible for neither of the above to return true
	 * in this case do nothing as the character is already square */
}

/* function to append/prepend white rows to an image to become square
 * mutates input
 *
 * @param input - the character vector to affix to
 * @param dimDiff - the difference of dimensions */
void affixWhiteRows(pixelData &input, int dimDiff) {
	// create new vector of desired dimensions
	pixelData temp(input.size(),vector<int>(input[0].size()+dimDiff));
	for (usint i = 0; i < temp[0].size(); i++) {
		for (usint j = 0; j < temp.size(); j++) {
			if (i < (usint)dimDiff/2) { // if upper affixed white row
				temp[j][i] = 1;
			} else if (i < input[0].size()+(int)dimDiff/2) { // leave be
				temp[j][i] = input[j][i-(int)dimDiff/2];
			} else { // if bottom affixed white row
				temp[j][i] = 1;
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
void affixWhiteCols(pixelData &input, int dimDiff) {
	// create new vector of desired dimensions
	pixelData temp(input.size()+dimDiff,vector<int>(input[0].size()));
	for (usint i = 0; i < temp[0].size(); i++) {
		for (usint j = 0; j < temp.size(); j++) {
			if (j < (usint)dimDiff/2) { // if left affixed white col
				temp[j][i] = 1;
			} else if (j < input.size()+(int)dimDiff/2) { // leave be
				temp[j][i] = input[j-(int)dimDiff/2][i];
			} else { // if right affixed white col
				temp[j][i] = 1;
			}
		}
	}
	input = temp; // mutate
}

/* function to remove whitespace from a character vector. Sometimes
 * you'll end up with white columns or rows on the extremes
 * of a character after segmentation: this algorithm removes these. 
 * Mutates input vector to be cropped as close to black pixels as possible
 *
 * @param input - the character vector to remove whitespace from */
void cullWhitespace(pixelData &input) {
	int actualHeight = input[0].size(); // init height of image
	int startingRow = 0; // first nonwhite row; init later
	bool flag = false; // to break out of nested loops
	for (usint i = 0; i < input[0].size(); i++) {
		for (usint j = 0; j < input.size(); j++) {
			if (input[j][i] == 0) {
				flag = true; // set flag T to break nested loop
				break; // break inner loop
			}
		}
		if (flag == true) {
			startingRow = i; // first nonwhite row
			break; // break outer loop
		} else {
			actualHeight--; // dec height as we need height sans white rows
		}
	}
	flag = false; // reset flag
	for (usint i = input[0].size()-1; i >= 0; i--) {
		for (usint j = 0; j < input.size(); j++) {
			if (input[j][i] == 0) {
				flag = true;
				break;
			}
		}
		if (flag == true) {
			break;
		} else {
			actualHeight--;
		}
	}
	// init vector of actual size of useful pixels
	pixelData temp(input.size(), vector<int>(actualHeight));
	for (usint i = 0; i < temp[0].size(); i++) {
		for (usint j = 0; j < temp.size(); j++) {
			temp[j][i] = input[j][startingRow + i];
		}
	}
	input = temp; // mutate
}

/* function to find horizontal distribution of pixel
 * values. Finds aggregate pixel value of all columns of
 * pixels in the image.
 *
 * @param input - the image vector to find distribution on
 * @param thresh - the threshold of noise
 * @return 1D vector of column distributions */
vector<int> findHorDistribution(pixelData &input, int thresh) {
	vector<int> blackDist(input.size()); // init vector of app. size
	for (usint hor = 0; hor < input.size(); hor++) {
		blackDist[hor] = 0; // initial value is zero
		for (usint ver = 0; ver < input[0].size(); ver++) {
			// sum all pixels values but invert so 0 = 255, 255 = 0
			blackDist[hor] += abs((input[hor][ver])-1);
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
vector<int> findVerDistribution(pixelData &input, int thresh) {
	vector<int> blackDist(input[0].size()); // init vector of app. size
	for (usint ver = 0; ver < input[0].size(); ver++) {
		blackDist[ver] = 0; // initial value is zero
		for (usint hor = 0; hor < input.size(); hor++) {
			// sum all pixel values but invert so 0 = 255, 255 = 0
			blackDist[ver] += abs((input[hor][ver])-1);
		}
		// set 0..1 instead of 0..n
		blackDist[ver] = (blackDist[ver] < thresh) ? 0 : 1;
	}
	return blackDist;
}

/* function to write each character vector to a file
 * vectors are flattened to 1D with dimensions prepending the characters
 *
 * @param input - a list of 2D vectors representing characters
 * @param filename - the filename to write to */
void writeToFile(queue<pixelData> &inList, string filename) {
	if (statusUpdates) {
		cout << "Writing " << filename.c_str() << " ... ";
	}
	ofstream outFile;
	outFile.open(filename.c_str());
	outFile << inList.size() << "\n"; // append number of chars to file
	pixelData temp; // temporary vector
	int maxChars = inList.size(); // number of chars in queue
	for (int i = 0; i < maxChars; i++) {
		temp = inList.front(); // access and init temp to first char
		inList.pop(); // can safely remove char from queue
		outFile << temp[0].size() << " "; // append height to file
		outFile << temp.size() << " "; // append width to file
		for (usint j = 0; j < temp[0].size(); j++) { 
			for (usint k = 0; k < temp.size(); k++) {
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

/* function to write .PGM intermediate files for diagnostic
 * purposes. Creates a .pgm of every segmented character.
 *
 * @param input - the character to write .pgm for */
void writePGM(pixelData &input) {
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
	imageOutput << "1" << "\n"; // depth, third header
	for (usint i = 0; i < input[0].size(); i++) {
		for (usint j = 0; j < input.size(); j++) {
			imageOutput << input[j][i] << " "; // insert pixel value
		}
		imageOutput << "\n";
	}
	imageOutput.close();
	if (statusUpdates) {
		cout << "done!" << endl;
	}
}

/* function to write to file the character index
 *
 * @param inList - a queue of posiitons
 * @param filename - the filename to write to */
void writeIndex(queue<char> &inList, string filename) {
	int temp = 0;
	if (statusUpdates) {
		cout << "Writing " << filename.c_str() << " ... ";
	}
	ofstream outFile;
	outFile.open(filename.c_str());
	while(inList.front() != 'e') { // while queue top is not EOF
		if (inList.front() == 's') { // if space
			outFile << " "; // write space
			inList.pop();
		} else if (inList.front() == 'n') { // if newline
			outFile << "\n"; // write newline
			inList.pop();
		} else if (inList.front() == 'c') { // if character
			// find number of successive 'c' in queue
			while(inList.front() == 'c') {
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

/* diagnostic tool for development, print an image's distribution
 *
 * @param dist - the distribution to print */
void printDist(vector<int> &dist) {
	for (usint i = 0; i < dist.size(); i++) {
		cout << dist[i] << " ";
	}
}

/* diagnostic tool for development, print an image vector
 *
 * @param input - the image vector to print */
void printVector(pixelData &input) {
	for (usint i = 0; i < input[0].size(); i++) {
		for (usint j = 0; j < input.size(); j++) {
			cout << input[j][i] << " ";
		}
		cout << "\n";
	}
	cout << "\n";
}
