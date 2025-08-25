import pyttsx3
import argparse
import traceback
import sys

#Initialize parser
parser = argparse.ArgumentParser()

#Adding optional argument
parser.add_argument("-t","--text",help="string input")
parser.add_argument("-l","--language",help="english or hindi")
parser.add_argument("-a","--accent",help="indian, australian, us & uk")
parser.add_argument("-g","--gender",help="male or female")
parser.add_argument("-i","--index",help="reader index, start from zero.")

#Read arguments from command line
args = parser.parse_args()

#Default Values

