from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

#initializing thre speech engine

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)# 0:male, 1:female
activationWord = 'computer'

#set path for chrome and conf the webbrowser
chromePath = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))

wolframaAppID = 'E42R3R-88YHH7GQA2'
wolframaClient = wolframalpha.Client(wolframaAppID)


#Method for allowing speech library

def speak(text, rate=120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

#Method for listening command

def parseCommand():
    listener = sr.Recognizer()
    print('Listening for your command')

    with sr.Microphone() as source:
        listener.pause_threshold = 2 #speech before it cancels in 2sec
        inputSpeech = listener.listen(source)

    try:
        print('Recognizing speech...')
        query = listener.recognize_google(inputSpeech, language='en_gb')
        print(f'Your command: {query}')
    except Exception as ex:
        print("I didn't quite catch that")
        
        print(ex)
        return 'None'
    return query

#method for wikipedia

def searchWikipedia(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('We are sorry invalid result.')
        return 'no result received'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as err:
        wikiPage = wikipedia.page(err.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

#Method for wolframalpha

#list of dictionary

def listDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']

def searchWolframalpha(query = ''):
    res = wolframaClient.query(query)
    #@success: wolfram Alpha was able to resolve the query
    #numpods: Number of results returned
    #pods: list of results, contains supods.

    if res['@success'] == 'false':
        return 'could not compute'
    
    else:
        result = ''#questions
        pod0 = res['pod'][0]
        pod1 = res['pod'][1]
        #contains the answer
        if(('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'.lower()]):
            result = listDict(pod1['subpod'])
            #remove the bracketed section
            return result.split('(')[0]
        else:
            question = listDict(pod0['subpod'])
            qsn = question.split('(')[0]
            speak('computation failed, querying universal databank')
            return searchWikipedia(qsn)

#Main loop

if __name__ == '__main__':
    speak('All systems nominal.')

    while True:
        query = parseCommand().lower().split()

        if query[0] == activationWord:
            query.pop(0)

            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings, all.')
                else:
                    query.pop(0) #remove 'say' word
                    speech = ''.join(query)
                    speak(speech)

            if query[0] == 'go' and query[1] == 'to':
                speak('Opening...')
                query = ''.join(query[2:])
                webbrowser.get('chrome').open_new(query)

            if query[0] == 'wikipedia':
                query = ''.join(query[1:])
                speak('Querying the universal databank')
                speak(searchWikipedia(query))

            if query[0] == 'compute' or query[0] == 'computer':
                query = ''.join(query[1:])
                speak('computing')
                try:
                    result = searchWolframalpha(query)
                    speak(result)
                except:
                    speak('the computer is unable to compute your command')

            if query[0] == 'log':
                speak('read to record your note')
                newNote = parseCommand().lower()
                with open('Recordtext.txt','w') as newFile:
                    newFile.write(newNote)
                    speak('Note written')

            if query[0] == 'exit':
                speak('Glad I helped')
                break





