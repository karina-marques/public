# Read a .xml file and generate a .ASC file
# June 24, 2022.

# Import libraries
import os
import os.path
import sys
import re
import xml.etree.ElementTree as ET
import numpy as np

# Define scale
scale = 2.5

# List all files
for root_dir, dirnames, filenames in os.walk(sys.argv[1]):
    for file in filenames:
        full_path = os.path.join(root_dir, file)
        name = re.search(r"(\d\d_L\d_[A-Z][a-z]?_\d\d)\.xml$", full_path)
        if not name:
            continue

        # Open and parse source file
        # Encoding should be UTF-8 in the .xml file. Otherwise, it will throw the following error
        # Multi byte encoding not supported
        tree = ET.parse(full_path)

        # Get the parent tat
        root = tree.getroot()

        # Read frame dimentions

        startX = float(root[0][1][0][0][0].text)
        startY = float(root[0][1][0][0][1].text)
        endX = float(root[0][1][0][0][2].text)
        endY = float(root[0][1][0][0][3].text)
        columns = int(root[0][1][0][0][5].text)
        rows = int(root[0][1][0][0][6].text)

        # Initializing target matrix with zeros
        cps = np.zeros((rows, columns), dtype=np.float64)

        # Read data and calculate counts per seconds
        for i in range(rows):
            line = root[0][1][0][i + 6].text.strip().split(',')
            for j in range(columns):
                cps[i][j] = float(line[j])
            line = root[0][1][0][i + 6 + rows].text.strip().split(',')
            for j in range(columns):
                cps[i][j] /= float(line[j])

        # Write the answer file
        with open(os.path.join(sys.argv[2], (name[1] + '.ASC')), 'w', encoding='utf-8') as answer:
            answer.write('ncols\t\t')
            answer.write(str(columns))
            answer.write('\nnrows\t\t')
            answer.write(str(rows))
            answer.write('\nxllcorner\t')
            answer.write(str(scale * columns * startX / abs(endX - startX)))
            answer.write(', ')
            answer.write(str(scale * columns * endX / abs(endX - startX)))
            answer.write('\nyllcorner\t')
            answer.write(str(scale * rows * startY / abs(endY - startY)))
            answer.write(', ')
            answer.write(str(scale * rows * endY / abs(endY - startY)))
            answer.write('\ncellsize\t')
            answer.write(str(scale))
            answer.write('\nNODATA_value\t-9999')
            for i in range(rows):
                answer.write('\n')
                for j in range(columns - 1):
                    answer.write(str(round(cps[i][j], 7)))
                    answer.write(' ')
                answer.write(str(cps[i][columns - 1]))