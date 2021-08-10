import os  # to save/open files
import speech_recognition as sr
import playsound  # to play saved mp3 file
from gtts import gTTS  # google text to speech


# **********************************************************************************************************#

num = 1

# read the given text (string) with help of Google Text To Speech
def assistant_speaks(string):
    global num

    # num to rename every audio file
    # with different name to remove ambiguity
    num += 1
    print("PerSon says: ", string)

    to_speak = gTTS(text=string, lang="en", slow=False)
    # saving the audio file given by google text to speech
    file = str(num) + ".mp3"
    to_speak.save(file)

    # playsound package is used to play the same file.
    playsound.playsound(file, True)
    os.remove(file)


# recognize the audio and turn it into string
def get_audio():
    r_object = sr.Recognizer()
    empty = ""

    with sr.Microphone() as source:
        print("Speak...")
        # recording the audio using speech recognition, limit 5 secs
        audio = r_object.listen(source, phrase_time_limit=5)
    print("Stop.")

    try:
        text = r_object.recognize_google(audio, language="en-US")  # string
        print("You said: ", text)
        return text
    except:
        assistant_speaks("Could not understand your command!")
        return empty


# open the txt files
def open_txt(string):
    text = str(string).lower()
    assistant_speaks("Opening Text Editor...")

    # open file
    if "parameter" in text:
        os.startfile("parameter.txt")
    elif "model" in text:
        os.startfile("models.txt")
    else:
        os.startfile("parameter.txt")
        os.startfile("models.txt")
    return


# find files of certain type under the current directory
def find_file(path, keyword):
    # list of all files
    lof = os.listdir(path)
    k = str(keyword)
    result = []

    for f in lof:
        if k in f:
            result.append(f)
    return result


# determine if an ordinal number has been declared
def get_key(string, dic):
    text = str(string).lower()

    try:
        # key = int
        value = []
        lok = list(dic.keys())
        lov = list(dic.values())

        for v in lov:
            for item in v:
                if item in text:
                    value = v
        key = lok[lov.index(value)]

    # catch ValueError when out of range
    except ValueError:
        key = 0

    return key


# **********************************************************************************************************#


# read the txt-files according to different commands
def read_txt(string, n=2):
    text = str(string).lower()

    # check out txt-files under the current directory
    path = os.getcwd()
    keyword = "txt"
    # list of txt files
    lof = find_file(path, keyword)
    names = [name.replace(".txt", "") for name in lof]
    # number of txt files
    nf = len(lof)

    count_0 = 0
    count_1 = 0
    count_2 = 0

    while count_0 <= n + 1:

        # shut down
        if "exit" in text or "bye" in text or "sleep" in text:
            assistant_speaks("Ending the process...")
            return

        if "both" in text:  # or ("model" in text and "parameter" in text)

            # read the entire content of models
            f1 = open("models.txt")
            lines = f1.readlines()
            for line in lines:
                assistant_speaks(line.strip("\n"))
            f1.close()
            # read the entire content of parameters
            f2 = open("parameter.txt")
            lines = f2.readlines()
            for line in lines:
                assistant_speaks(line.strip("\n"))
            f2.close()
            return

        if "model" in text:

            # read the whole content of models
            f = open("models.txt")
            lines = f.readlines()
            for line in lines:
                assistant_speaks(line.strip("\n"))
            f.close()
            return

        if "parameter" in text:

            # dictionary of ordinal number and keywords
            # ##########################################
            # ###...how to generate automatically?...###
            # ##########################################
            d = {
                1: ["one", "1", "first"],
                2: ["two", "2", "second"],
                3: ["three", "3", "third"],
                4: ["four", "4", "fourth"],
            }

            # load the file and get the basic information
            f = open("parameter.txt")
            lines = f.readlines()
            nl = len(lines)

            while count_1 <= n + 1:
                key = get_key(text, d)

                # shut down
                if "exit" in text or "bye" in text or "sleep" in text:
                    assistant_speaks("Ending the process...")
                    return

                # ########################################################################
                # ###...judge "all model and parameter" / "model and all parameter"?...###
                # ########################################################################
                if "all" in text or "entire" in text:

                    # read the whole content of parameters
                    f = open("parameter.txt")
                    lines = f.readlines()
                    for line in lines:
                        assistant_speaks(line.strip("\n"))
                    f.close()
                    return

                # when no ordinal number has been declared
                elif key == 0:

                    count_1 += 1
                    if count_1 < n + 1:
                        speach_1 = """There are {} groups of parameter available, which one would you like to check out?""".format(
                            nl
                        )
                        assistant_speaks(speach_1)
                        text = (
                            get_audio().lower()
                        )  # <------------------------- audio input
                        # text = "fourth"
                    else:
                        pass

                # key != 0, when an ordinal number has been declared 
                else:

                    if key <= nl:

                        # read a certain row of parameter
                        key = int(key) - 1
                        assistant_speaks(lines[key].strip("\n"))
                        f.close()
                        return

                    # when key > nl
                    else:

                        while count_2 <= n + 1:
                            key = get_key(text, d)

                            if "exit" in text or "bye" in text or "sleep" in text:
                                assistant_speaks("Ending the process...")
                                return
                            if key <= nl:
                                break
                            else:
                                count_2 += 1
                                if count_2 < n + 1:
                                    speach_2 = """Out of search boundary, there are {} groups of parameter available, please try again.""".format(
                                        nl
                                    )
                                    assistant_speaks(speach_2)
                                    text = (
                                        get_audio().lower()
                                    )  # <------------------------- audio input
                                    # text = "third"
                                else:
                                    pass
                            
                        # when count_2 > n + 1
                        else:
                            
                            speach_3 = """Can not execute your command, do you want me to open the file?"""
                            assistant_speaks(speach_3)
                            ans = (
                                get_audio().lower()
                            )  # <------------------------- audio input
                            # ans = "yes"
                            if "yes" in ans:
                                open_txt("parameter.txt")
                                return
                            else:
                                assistant_speaks("Ending the process...")
                                return
                        
            # when count_1 > n + 1
            else:
                count_0 += 1
                pass
            
        # when command not executable
        else:
            
            count_0 += 1
            if count_0 < n + 1:
                speach_0 = """There are {} files available, {}, which one would you like to check out?""".format(
                    nf, names
                )
                assistant_speaks(speach_0)
                text = get_audio().lower()  # <------------------------- audio input
                # text = "parameter"
            else:
                pass
            
    # when count_0 > n + 1
    else:
        speach = """Can not execute your command, ending the process..."""
        assistant_speaks(speach)
        return


# read_txt("read something", 2)


# **********************************************************************************************************#


# execute actions
def process_text(string, n=2):
    text = str(string).lower()
    count = 0

    while count < n + 1:

        if "open" in text:
            open_txt(text)
            return

        elif "read" in text:
            # two arguments required, string and a number of attempts
            read_txt(text, 2)
            return

        elif "path" in text:
            assistant_speaks("The file is ...")
            # ############################################################
            # ### ...search in computer or do anything else you want...###
            # ############################################################
            return

        else:
            count += 1
            if count < n + 1:
                assistant_speaks("Can not execute your command, please try again.")
                text = get_audio().lower()
                # text = "blabla"
            else:
                pass

    else:
        assistant_speaks("Can not execute your command, ending the process...")
        return


# Driver Code
if __name__ == "__main__":

    while True:
        assistant_speaks("What can i do for you?")
        # turn all letters in string into lowercase
        text = get_audio().lower()

        if "who are you" in text or "what can you do" in text:
            speach = """Hello, I am Person. Your personal Assistant. 
            I am here to read the parameters or models for you."""
            assistant_speaks(speach)
            continue

        if "exit" in text or "bye" in text or "sleep" in text:
            # only work in this loop
            assistant_speaks("Ok bye")
            break

        if text == "":
            continue

        else:
            # calling process text to process the query
            process_text(text)
            break
