# Import libraries
# from PIL import Image хуже распознается
import cv2 
import pytesseract 
import sys 
import os 
import argparse
from import_to_db import text_to_db


parser = argparse.ArgumentParser(description='OCR')
parser.add_argument('in_filenames', help='Input filenames')
parser.add_argument('out_filename', help='Output filename')


def Pic2Txt(listImg, outfile, cursor):

	if not os.path.exists(outfile):
		os.mkdir(outfile)
	# Iterate through all the image
	for img in listImg:

		f = open(str(outfile) + '/' + str(os.path.basename(img).split('.')[0]) + '.txt', "a")
		# Recognize the text as string in image using pytesserct

		text = str(((pytesseract.image_to_string(cv2.imread(img),lang = 'eng+rus')))) #'eng+rus'

		# The recognized text is stored in variable text 
		# Any string processing may be applied on text 
		# Here, basic formatting has been done: 
		# In many PDFs, at line ending, if a word can't 
		# be written fully, a 'hyphen' is added. 
		# The rest of the word is written in the next line 
		# Eg: This is a sample text this word here GeeksF- 
		# orGeeks is half on first line, remaining on next. 
		# To remove this, we replace every '-\n' to ''. 
		text = text.replace('-\n', '')	 

		# Finally, write the processed text to the file. 
		#with open(fname, "w", encoding="utf-8") as f:
		f.write(text)
		f.close()
		text_to_db(text, str(os.path.abspath(img)), cursor)

	# Close the file after writing all the text. 


if __name__ == '__main__':
	args = parser.parse_args()
	Pic2Txt(args.in_filenames.split(','), args.out_filename)