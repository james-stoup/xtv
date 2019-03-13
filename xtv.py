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
   LIGHT_GRAY_BG = '\033[47m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'



def print_children(child, offset):
   """ Recursivly print the data, adding an offset for every level """
   kids = child.find('.')

   # Only print the children if there are any
   if len(list(kids)):
      for k in kids:
         print_string = ''

         # make the main tags bold
         if k.tag:
            print_string += (color.BOLD  + k.tag + ':' + color.END + ' ')

         # not everything has text and white space doesn't count
         if k.text:
            clean_text = k.text.lstrip()
            if clean_text:
               print_string += ('%s ' % clean_text)

         # the attributes are almost always going to be a map
         if k.attrib:
            if hasattr(k.attrib, "__len__"):
               for key, value in k.attrib.items():
                  tmp_str = '(' + key + ': ' + value + ')'
                  tmp_len = len(tmp_str) + offset + 4
                  att_str = tmp_str.rjust(tmp_len)
                  print_string += '\n' + att_str

         # add to the offset each level down we go
         str_len = len(print_string) + offset
         new_string = print_string.rjust(str_len)
         print new_string

         # woo hoo, recursion
         print_children(k, offset + 4)


def main():
   """ Parse cli args and print the cleaned up XML """

   # yeah, need to actually handle args...
   args = sys.argv
   xml_file = args[1]

   # turn the file into a tree
   tree = ET.parse(xml_file)
   root = tree.getroot()

   # I like the root node to be red, but I suppose I could add a no-color flag
   root_str = '=== ' + root.tag + ' ==='
   root_str_len = len(root_str)
   header_str = ''
   for x in range(root_str_len):
      header_str += '='

   print header_str
   print color.BLACK + color.BOLD + root_str + color.END
   print header_str

   for child in root:
      print color.LIGHT_GRAY_BG + color.BOLD + child.tag + color.END
      print_children(child, 4)
      print ''



if __name__ == '__main__':
   main()
