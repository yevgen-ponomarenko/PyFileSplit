#!/usr/bin/env python
import sys, argparse
from PyPDF2 import PdfFileReader, PdfFileWriter

parser = argparse.ArgumentParser("Produces big PDF file by multiplying merging existing up to the pages limit")
parser.add_argument("--input-file", "-f", type=argparse.FileType('rb'), help="input file")
parser.add_argument("--pages-number", "-p", type=int, help="number of pages in output file")
parser.add_argument("--output-file", "-out", type=str, help="output file name")

def pdf_cat(input_file, output_page_numbers, output_stream):    
    # First open all the files, then produce the output file, and
    # finally close the input files. This is necessary because
    # the data isn't read from the input files until the write
    # operation. Thanks to
    # https://stackoverflow.com/questions/6773631/problem-with-closing-python-pypdf-writing-getting-a-valueerror-i-o-operation/6773733#6773733        
    reader = PdfFileReader(input_file)
    writer = PdfFileWriter()

    input_page_numbers = reader.getNumPages()
    inserted_pages = 0

    while inserted_pages < output_page_numbers:
        index =  inserted_pages if inserted_pages < input_page_numbers else inserted_pages % input_page_numbers
        writer.addPage(reader.getPage(index))
        inserted_pages+=1
    
    writer.write(output_stream)

if __name__ == '__main__':
    args = parser.parse_args()
    input_file = args.input_file
    output_file = open(args.output_file, 'wb')
    try:
        pdf_cat(input_file, args.pages_number, output_file)
    finally:
        input_file.close()
        output_file.close()
    