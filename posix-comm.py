#!/usr/bin/python

"""
Implements the POSIX comm command.

$Id: comm.py,v 1.0 2017/10/21 23:34:00 iguelmamene Exp $
"""

import random, sys, string, locale
from optparse import OptionParser

class implementcomm:
    def __init__(self, file1, file2, line1, line2, line3, isunsorted):

	if file1 == "-": # read from stdin
	   self.list_1 = sys.stdin.readlines()
	else:
	   f1 = open(file1, 'r')
	   self.list_1 = f1.readlines()
	   f1.close()

	if file2 == "-": # read from stdin
	   self.list_2 = sys.stdin.readlines()
	else:
	   f2 = open(file2, 'r')
           self.list_2 = f2.readlines()
           f2.close()

        self.results_list = []	# columns to be outputted

	if isunsorted: # algorithm for unsorted files
	   for x in self.list_1[:]:
	      if x in self.list_2:
                 self.results_list.append("\t\t" + x)
	       	 self.list_2.remove(x)
	      else:
                 self.results_list.append(x)
           for y in self.list_2[:]:
              self.results_list.append("\t" + y)

        else: # algorithm for sorted files
           while (self.list_1 and self.list_2):
              if self.list_1[0] == self.list_2[0]:
                 self.results_list.append("\t\t" + self.list_1[0])
                 self.list_1.remove(self.list_1[0])
                 self.list_2.remove(self.list_2[0])
              elif self.list_1[0] < self.list_2[0]:
                 self.results_list.append(self.list_1[0])
                 self.list_1.remove(self.list_1[0])
              elif self.list_2[0] < self.list_1[0]:
                 self.results_list.append("\t" + self.list_2[0])
                 self.list_2.remove(self.list_2[0])
           if self.list_2:
              for i in self.list_2[:]:
                 self.results_list.append("\t" + i)
           elif self.list_1:
              for i in self.list_1[:]:
                 self.results_list.append(i)

        if line1 and line2: # user only wants to print column 3
           self.results_list[:] = [ x for x in self.results_list if "\t\t" in x ]
           x = len(self.results_list) - 1
           while (x >= 0):
              if "\t\t" in self.results_list[x]:
                 self.results_list[x]  = self.results_list[x].replace("\t\t", "", 1)
              x = x - 1
        elif line1 and line3: # user only wants to print column 2
           x = len(self.results_list) - 1
           while (x >= 0):
              if "\t\t" in self.results_list[x]:
                 self.results_list[x]  = self.results_list[x].replace("\t\t", "", 1)
              x = x - 1
           self.results_list[:] = [ x for x in self.results_list if "\t" in x ]
           x = len(self.results_list) - 1
           while (x >= 0):
              if "\t" in self.results_list[x]:
                 self.results_list[x]  = self.results_list[x].replace("\t", "", 1)
              x = x - 1
        elif line2 and line3: # user only wants to print column 1
           self.results_list[:] = [ x for x in self.results_list if "\t" not in x ]
        elif line1: # user only wants to print columns 2 and 3
           self.results_list[:] = [ x for x in self.results_list if "\t" in x ]
           x = len(self.results_list) - 1
           while (x >= 0):
              if "\t" in self.results_list[x]:
                 self.results_list[x]  = self.results_list[x].replace("\t", "", 1)
              x = x - 1
        elif line2: # user only wants to print columns 1 and 3
           self.results_list[:] = [ x for x in self.results_list if "\t\t" in x or ("\t" not in x) ]
           x = len(self.results_list) - 1
           while (x >= 0):
              if "\t" in self.results_list[x]:
                 self.results_list[x]  = self.results_list[x].replace("\t\t", "\t", 1)
              x = x - 1
        elif line3: # user only wants to print columns 1 and 2
           self.results_list[:] = [ x for x in self.results_list if "\t\t" not in x ]

        if line1 and line2 and line3: # do not print anything if the user wants to suppress all three columns
           n = 0
        else: # print the desired columns
           for i in self.results_list[:]:
              sys.stdout.write(i)
def main():
    version_msg = "%prog 2.0"
    usage_msg = """%prog [OPTION]... file1 file2

select or reject lines common to two files"""

    parser = OptionParser(version=version_msg, usage=usage_msg)

    # add options -1, -2, -3, and -u

    parser.add_option("-1", action="store_true", dest="suppress_line1", default=False,
                      help="Suppress printing of column 1.") # option -1

    parser.add_option("-2", action="store_true", dest="suppress_line2", default=False,
                      help="Suppress printing of column 2.") # option -2

    parser.add_option("-3", action="store_true", dest="suppress_line3", default=False,
                      help="Suppress printing of column 3.") # option -3

    parser.add_option("-u", action="store_true", dest="file_unsorted", default=False,
                      help="Passing unsorted files to the script when -u is set will not cause undefined behavior.") # option -u

    options, args = parser.parse_args(sys.argv[1:])

    try:
        suppress_line1 = bool(options.suppress_line1)
    except:
        parser.error("invalid option: {0}".
                     format(options.suppress_line1))

    try:
        suppress_line2 = bool(options.suppress_line2)
    except:
        parser.error("invalid option: {0}".
                     format(options.suppress_line2))

    try:
        suppress_line3 = bool(options.suppress_line3)
    except:
        parser.error("invalid option: {0}".
                     format(options.suppress_line3))

    try:
        file_unsorted = bool(options.file_unsorted)
    except:
        parser.error("invalid option: {0}".
                     format(options.file_unsorted))

    if len(args) != 2:
        parser.error("wrong number of operands")

    file_1 = args[0] # extract arguments
    file_2 = args[1]

    if file_1 == "-": # both files cannot be read from stdin
       if file_2 == "-":
          parser.error("cannot read both files from stdin, as both files cannot be denoted by -")

    try:
       comp_var = implementcomm(file_1, file_2, suppress_line1, suppress_line2, suppress_line3, file_unsorted)
    except IOError as err:
       (errno, strerror) = err.args
       parser.error("I/O error({0}): {1}".
                     format(errno, strerror))


if __name__ == "__main__":
    main()
