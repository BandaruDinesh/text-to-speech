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
    language=str(args.language).lower()
    if language=="hindi" and not args.accent:
        # prefer Indian accent for Hindi unless user explicitly set one
        accent="indian"

#if accent args passed in cli
if args.accent:
    accent=str(args.accent).lower()

#if gender args passed in cli
if args.gender:
    gender=str(args.gender).lower()

#filters the languages and accents
def filter_rule(voice, gender, language, accent, default):
    # normalize desired tag like 'en_US'
    desired = (language.lower() + '_' + accent.upper())
    # pull languages from voice.language or voice.languages, normalize bytes/strings
    langs = getattr(voice, 'language', None)
    if langs is None:
        langs = getattr(voice, 'languages', [])
    if not isinstance(langs, (list, tuple)):
        langs = [langs]
    norm_tags = []
    for t in langs:
        try:
            if isinstance(t, bytes):
                t = t.decode('utf-8', errors='ignore')
            t = str(t).strip().replace('-', '_')
            if '_' in t:
                ll, rr = t.split('_', 1)
                t = ll.lower() + '_' + rr.upper()
            else:
                t = t.lower()
            norm_tags.append(t)
        except Exception:
            pass
    # gender (case-insensitive) — if engine lacks gender, don't block
    vg = (getattr(voice, 'gender', '') or '').lower()
    gender_ok = (vg == '') or (vg in [g.lower() for g in gender])
    if default:
        return gender_ok and (desired in norm_tags)
    return (desired in norm_tags) or (getattr(voice, 'name', '') in ["default","Alex"])

#filtering voices based on given criteria
def filter_voice(voices,gender,language,accent,default=True):
    filter_list =[voice for voice in voices if filter_rule(voice,gender,language,accent,default)]
    if len(filter_list):
        return filter_list
    if default:
        return filter_voice(voices,gender,language,accent,False)
    return []

#update reader's language,accent and gender
def update_language(reader,language,accent,gender):
    #Audio Type Selection Criteria
    languages={"english":"en","hindi":"hi"}
    accents ={"indian":"IN","us":"US","australian":"AU","uk":"GB"}
    genders={"male":["voiceGenderMale","male"],"female":["voiceGenderFemale","female"],"none":["None"]}

    #getting list of filtered voices based on selection criteria
    filtered_voice_list=filter_voice(
        reader.getProperty('voices'),
        genders.get(gender, genders["none"]),
        languages.get(language, "en"),
        accents.get(accent, "US")
    )

    if len(filtered_voice_list):
        #Displaying the details of filtered voices
        print("AVAILABLE READERS")
        for index,voice in enumerate(filtered_voice_list):
            print("\nVoice Index : %d" % index)
            print("ID: %s" % voice.id)
            print("Name: %s" % voice.name)
            print("Gender: %s" % voice.gender)
            print("Language: %s" % (getattr(voice, "language", getattr(voice, "languages", "unknown"))))

        index =0
        try:
            if args.index and filtered_voice_list[int(args.index)]:
                index =int(args.index)
        except IndexError:
            pass
        print("\n%s is reading for you." % filtered_voice_list[index].name)
        #applying the voice of selected reader
        reader.setProperty('voice',filtered_voice_list[index].id)
    else:
        print("No reader available. \nAlex is reading for you.")

if not args.text:
    try:
        text_to_read = input("Type text to speak: ").strip() or text_to_read
    except EOFError:
        pass

try:
    # initialize the reading engine
    reader = pyttsx3.init()

    #updating readers language, accent and gender before reading text.
    update_language(reader,language,accent,gender)

    #read the given text
    reader.say(text_to_read)

    #Execution of reading process
    reader.runAndWait()

    #Finish the reading process
    reader.stop()

except OSError as error:
    traceback.print_exception(*sys.exc_info())
    print("There is a chance that some required system lib and try again")
except Exception as error:
    traceback.print_exception(*sys.exc_info())
    print("something went wrong; please report the issue at https://github.com/BandaruDinesh/text-to-speech/issues")












