# posix-comm
This project implements the POSIX command comm, which compares two files. This implementation supports the options -1, -2, -3, -u, and all their combinations (Python).

The first column of output consists of lines unique to the first file. The second column consists of lines unique to the second file. The third column consists of lines that appear in both files. The options -1, -2, and -3 suppress the printing of columns 1, 2, and 3, respectively. The option -u allows for comparison of unsorted files. If -u is unspecified, it is assumed that the two files are sorted.
