#!/usr/bin/env python

import sys
import csv
import xml.etree.ElementTree as ET

class color:
   BLACK = '\033[30m'
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


args = sys.argv
xml_file = args[1]

tree = ET.parse(xml_file)
root = tree.getroot()

def print_children(child, offset):
    #print '%s - %s' % (child.tag, child.attrib)

    kids = child.find('.')

    if len(list(kids)):
        for k in kids:
            print_string = ''

            if k.tag:
                print_string += (color.BOLD  + k.tag + ':' + color.END + ' ')

            if k.text:
                clean_text = k.text.lstrip()
                if clean_text:
                    print_string += ('%s ' % clean_text)

            if k.attrib:
                if hasattr(k.attrib, "__len__"):
                    for key, value in k.attrib.items():
                        tmp_str = '(' + key + ': ' + value + ')'
                        tmp_len = len(tmp_str) + offset + 4
                        att_str = tmp_str.rjust(tmp_len)
                        print_string += '\n' + att_str
                else:
                    print_string += ('%s ' % k.attrib)

            str_len = len(print_string) + offset
            new_string = print_string.rjust(str_len)
            print new_string

            print_children(k, offset + 4)


print color.RED + color.BOLD + '=== ' + root.tag + ' ===' + color.END

for child in root:
    print color.BLUE + color.BOLD + child.tag + color.END
    print_children(child, 2)
    print ''
