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
text_to_read ="Hi there! I'll read text for you."
gender ="male"
language="english"
accent="us"

#if text args passed in cli
if args.text:
    text_to_read=args.text

#if language args passed in cli
if args.language:
    language=args.language
    if language=="hindi":
        accent="Indian"

#if accent args passed in cli
if args.accent:
    accent=args.accent

#if gender args passed in cli
if args.gender:
    gender=args.gender

#filters the languages and accents
def filter_rule(voice,gender,language,accent,default):
    if default:
        return voice.gender in gender and voice.language[0]==(language + '_' +accent)
    return  voice.language[0]==(language + '_' +accent) or voice.name in ["default","Alex"]

#filtering voices based on given criteria
def filter_voice(voices,gender,language,accent,default=True):
    filter_list =[voice for voice in voices if filter_rule(voice,gender,language,accent,default)]
    if len(filter_list):
        return filter_list
    return filter_voice(voices,gender,language,accent,False)

#update reader's language,accent and gender
def update_language(reader,language,accent,gender):
    #Audio Type Selection Criteria
    languages={"english":"en","hindi":"hi"}
    accents ={"indian":"IN","us":"US","australia":"AU","uk":"GB"}
    genders={"male":["voiceGenderMale","male"],"female":["voiceGenderFemale","female"],"none":["None"]}

    #getting list of filtered voices based on selection criteria
    filtered_voice_list=filter_voice(reader.getproperty('voices'),genders[gender],languages[language],accents[accent])

    if len(filtered_voice_list):
        #Displaying the details of filtered voices
        print("AVAILABLE READERS")











