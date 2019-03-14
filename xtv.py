#!/usr/bin/env python

# An XML Terminal Viewer
# Author: James Stoup
# Date: 14 MAR 2019
# This should be backwards compatible
# all the way to python 2.7

import sys
import csv
import xml.etree.ElementTree as ET
import optparse
import time
import os


# Keep some colors around in case we add more later
class color:
   BLACK         = '\033[30m'
   BLUE          = '\033[94m'
   CYAN          = '\033[96m'
   DARK_CYAN     = '\033[36m'
   GREEN         = '\033[92m'
   LIGHT_GRAY_BG = '\033[47m'
   PURPLE        = '\033[95m'
   RED           = '\033[91m'
   YELLOW        = '\033[93m'

   UNDERLINE     = '\033[4m'
   BOLD          = '\033[1m'
   END           = '\033[0m'

   
# Helper class used only for printing the help examples
class MyParser(optparse.OptionParser):
    def format_epilog(self, formatter):
        return self.epilog

     

def print_children(child, offset, plain):
   """ Recursivly print the data, adding an offset for every level """
   kids = child.find('.')

   # Only print the children if there are any
   if len(list(kids)):
      for k in kids:
         print_string = ''

         # make the main tags bold
         if k.tag:
            if plain:
               print_string += (k.tag + ': ')
            else:
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
         print_children(k, offset + 4, plain)



def setup_parser():
   """ Setup the option & arguement parser """
   epilog_str = """
Examples:

  ### View an xml file in a human readable way
  ./xtv.py <xml-file-to-read>

"""

   parser = MyParser(epilog = epilog_str,
                     usage='usage: %prog [options]',
                     version='%prog 1.0.0')
   
   # import flag
   parser.add_option('-p', '--plain',
                     action='store_true',
                     dest='plain_view_flag',
                     default=False,
                     help='Display output with no additional formatting or color')

   (options, args) = parser.parse_args()

   return (options, args)

         
def main():
   """ Print the cleaned up XML """

   # This shoudl be stupid simple as you only pass in one file
   (opts, args) = setup_parser()
   if len(args) < 1:
      print 'YOU DONE MESSED UP A-A-RON! (must supply an xml file to parse)'
      sys.exit()
   elif len(args) > 1:
      print 'YOU DONE MESSED UP A-A-RON! (too many arguements passed in)'
      sys.exit()

   # If they don't want fancy printing turn it off
   plain = False
   if opts.plain_view_flag:
      plain = True

   # turn the file into a tree
   xml_file = args[0]
   tree = ET.parse(xml_file)
   root = tree.getroot()

   # Print a nice header showing the root node
   root_str = '=== ' + root.tag + ' ==='
   root_str_len = len(root_str)
   header_str = ''
   for x in range(root_str_len):
      header_str += '='

   print header_str
   if plain:
      print root_str
   else:
      print color.BOLD + root_str + color.END
   print header_str

   for child in root:
      if plain:
         print child.tag
      else:
         print color.LIGHT_GRAY_BG + color.BOLD + child.tag + color.END
      print_children(child, 4, plain)
      print ''



if __name__ == '__main__':
   main()
