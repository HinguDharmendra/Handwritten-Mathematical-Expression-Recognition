import sys
import time

import stroke_level_parser
import symbol_level_parser

__author__ = ['Dharmendra Hingu', 'Sanjay Khatwani']

"""
This program processes one inkml file and produces output lg file.
"""

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("This file needs two arguments: path to text file, symbol/stroke. Where "
              "B/T = B for bonus set file and T for testing set file.")
    else:
        start = time.time()
        if str(sys.argv[2]) == 'symbol':
            symbol_level_parser.main(sys.argv[1])
        elif str(sys.argv[2]) == 'stroke':
            stroke_level_parser.main(sys.argv[1])
        print("The predicted lg file is present in: ", str(sys.argv[1]).
              replace('.inkml', '.lg'))
        print("Time taken to process this file: ", time.time() - start,
              " seconds")
