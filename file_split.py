#!/usr/bin/env python
import sys, argparse, datetime
from PyPDF2 import PdfFileReader, PdfFileWriter
from os.path import basename, splitext

parser = argparse.ArgumentParser("Produces big PDF file by multiplying merging existing up to the pages limit")
parser.add_argument("--input-file", "-f", type=argparse.FileType('rb'), help="input file")
parser.add_argument("--output-name-format", "-n", type=str, help="output files name format - [{0}:file name, {1}: index]", default="results/splitted_{0}_{1}.pdf")
parser.add_argument("--start-page", "-start", type=int, help="start page index [0..N]", default=0)
parser.add_argument("--end-page", "-end", type=int, help="end page index", default=-1)
parser.add_argument("--split-every-pages", "-p", type=int, help="split by pages")

def pdf_split(input_file, start, end, page_num, name_pattern):         
    reader = PdfFileReader(input_file)    
    file_name = splitext(basename(args.input_file.name))[0]

    current_inserting_page = 0    
    insert_up_to = end if end > 0 and reader.getNumPages() >= end else reader.getNumPages()

    writer = PdfFileWriter()
    current_writing_file_index = 1   

    print()
    start_time = datetime.datetime.now()    

    while current_inserting_page < insert_up_to:        
        if current_inserting_page > 0 and current_inserting_page % page_num == 0:
            current_writing_file = open(name_pattern.format(file_name, current_writing_file_index), 'wb')
            writer.write(current_writing_file)
            current_writing_file.close()
            current_writing_file_index+=1
            writer = PdfFileWriter()

            if (current_writing_file_index - 1) % 100 == 0:
                print('Generated #{0} files. Elapsed time {1}'.format(current_writing_file_index - 1, str(datetime.datetime.now() - start_time)))
        
        writer.addPage(reader.getPage(current_inserting_page))
        current_inserting_page+=1

    if writer.getNumPages() > 0:
        current_writing_file = open(name_pattern.format(file_name, current_writing_file_index), 'wb')
        writer.write(current_writing_file)
        current_writing_file.close()
    print('Whole split elapsed time {0}'.format(str(datetime.datetime.now() - start_time)))

if __name__ == '__main__':
    args = parser.parse_args()
    input_file = args.input_file
    try:
        pdf_split(input_file, args.start_page, args.end_page, args.split_every_pages, args.output_name_format)
    finally:
        input_file.close()
        
    