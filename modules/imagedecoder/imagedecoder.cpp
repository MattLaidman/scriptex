//compile with
// g++ -fPIC -shared `Magick++-config --cppflags --cxxflags --ldflags --libs` -o modules/imagedecoder/imagedecoder.so modules/imagedecoder/imagedecoder.cpp
//Module 1: Image Decoding

  #include "imagedecoder.h"

  //Sets the file name based on the infile name provided by the runner
  void ImageDecoder::SetThreshold(int th){
    threshold = th;
  }  
  void ImageDecoder::SetFileName(string name){
    FileName = name;
  }
  //used to set the rows and columns from the image
  void ImageDecoder::SetRowCol(int x, int y){
    rows = x;
    columns = y;
  }
  /* Converts the image
    takes the output file name passed from the runner class
	It also accepts a boolean which is passed from the user
	The boolean is to check and see if there are lines on the page
	if there are lines the program will ignore a color quantum and only read 2
	in order to blank out the lines 
  */
  void ImageDecoder::ConvertImage(string output){
    r = 0;
    try {
        //used to write the file
        ofstream myfile;
        //reads the image based on the file name set in SetFileName
        Image image(FileName);
        //sets the row and columns as extracted from the image
      SetRowCol((image).rows(),(image).columns());
      /*The range of colors in the image is then calculated by getting the value of 2 to the exponent of the images’ modulus depth,
        which is the minimum number of bits required to support the RGB of the image without losing accuracy.
      */
      int quantumRange = pow(2, image.modulusDepth());
      //the pixels are extracted fromt the image
      Pixels view(image);
      //array of pixels are built from the view, which are the pixels from the image
      PixelPacket *pixels = view.get(0,0,columns,rows);
      //opens up the file that will be written to based on the string input passed to the method
      myfile.open(output.c_str());
      //writes the width and length of the image for module 2
      myfile <<columns << " " << rows << "\n";
      //two for loops that run the height and width of the image
          for(int row = 0; row < rows; row++){
            for(int col = 0; col < columns; col++){
              //gets the current colour of the pixel the for loops are on
              Color color = pixels[columns * row + col];
              //the red green and blue values are stored in three seperate integers
              //GrayscaleType was set to the image earlier, but it was causing some errors
			  //if there are lines present on the page it will ignore the red quantum 
              if(lines){
                  r = (color.redQuantum()/quantumRange);
                }
                g = (color.greenQuantum()/quantumRange);
                b = (color.blueQuantum()/quantumRange);
              //the average is taken, and written to an image.
              int intRGB = (r+g+b)/3;
              //The earlier threshold of 127 was causing it to look too washed out, 200 spit out a pretty good image.
              //A variable can be set to fool around with the image contrast
              if(intRGB < threshold)
              myfile <<"0 ";
              else
              myfile <<"1 ";
            }
            myfile << endl;

          }
          myfile.close();

    }
    catch( Exception &error_ )
      {
        cout << "Caught exception: " << error_.what() << endl;
      }
  }

//runner for the module, takes the infile name, outfile name, and if there are lines or not
ImageDecoder::ImageDecoder(string infile, string outfile){
    if(lines){
        SetThreshold(127);
    } else {
        SetThreshold(200);
    }
    SetFileName(infile);
    ConvertImage(outfile);
}


void _decodeImage(string infile, string outfile) {
  ImageDecoder decoder(infile, outfile);
}