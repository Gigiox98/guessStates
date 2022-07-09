import os
from pathlib import Path
import random
import time
import json

def throwDice(beginNumber,endNumber):
    #Per generare il numero si utilizza l'algoritmo Mersenne Twister: A 623-dimensionally equidistributed uniform pseudorandom number generator”.
    result = random.randint(beginNumber,endNumber)
    time.sleep(0.5)
    return result

def functionAccettableValues(values):
    print('I valori accettabili sono: '+values)
    return input().lower()
    
def functionAccettableValuesCaseSensitive(values):
    print('I valori accettabili sono: '+values)
    return input()
    
def returnLoopResponse(acceptableValues,response):
    for value in acceptableValues:
        if(response == value):
            return False
    return True
    
def loopQuestion(question,acceptableValues):
    print(question)
    indexValue = 0
    stringValues = '';
    for value in acceptableValues:
        if indexValue == len(acceptableValues)-1:
            stringValues += value.lower()
        else:
            stringValues += value.lower() +", "
        indexValue += 1
    response = functionAccettableValues(stringValues)
    while(returnLoopResponse(acceptableValues,response)):
        print()
        print('Hai inserito un valore non accettabile, riprova')
        response = functionAccettableValues(stringValues)
    return response
    

def loopQuestionCaseSensitiveWithoutChecks(question):
    print(question)
    return input()
   
userPathHome = str(Path.home()).replace("\\","/")
if not os.path.exists(userPathHome+'/pathsJson.txt'):
    absolute_path = loopQuestionCaseSensitiveWithoutChecks('Inserisci il path assoluto del tuo file di testo con struttura JSON')
    newFile = open(userPathHome+'/pathsJson.txt', 'w')
    newFile.write(absolute_path+"\n")
    newFile.close()
    insertNewPathResponse = loopQuestion("Vuoi inserire un altro file?",['si','no'])
    while (insertNewPathResponse == 'si'):
        absolute_path = loopQuestionCaseSensitiveWithoutChecks('Inserisci il path assoluto del tuo file di testo con struttura JSON')
        newFile = open(userPathHome+'/pathsJson.txt', 'a')
        newFile.write(absolute_path.replace("\\","/")+"\n")
        newFile.close()
        insertNewPathResponse = loopQuestion("Vuoi inserire un altro file?",['si','no'])
else:
    print('Sono già presenti dei file con la struttura JSON richiesta\n')
    time.sleep(0.5)
    insertNewPathResponse = loopQuestion("Vuoi inserire un nuovo file?",['si','no'])
    while (insertNewPathResponse == 'si'):
        absolute_path = loopQuestionCaseSensitiveWithoutChecks('Inserisci il path assoluto del tuo file di testo con struttura JSON')
        newFile = open(userPathHome+'/pathsJson.txt', 'a')
        newFile.write(absolute_path.replace("\\","/")+"\n")
        newFile.close()
        print()
        insertNewPathResponse = loopQuestion("Vuoi inserire un altro file?",['si','no'])
   
score = 0
rematchResponse = 'si'
while (rematchResponse == 'si'):
    filePathsJson = open(userPathHome+'/pathsJson.txt','r')
    lines = filePathsJson.readlines()
    print('Sono presenti questi file di testo con la struttura JSON richiesta\n')
    lineIndex = 1
    lineIndexValues = []
    lineIndexValuesString = ''
    for line in lines:
        lineIndexValues.append(str(lineIndex))
        if len(lines) == lineIndex:
            lineIndexValuesString += str(lineIndex)
        else:
            lineIndexValuesString += str(lineIndex) + ', '
        print (str(lineIndex)+'. '+line.replace("\n",""))
        lineIndex += 1

    print()

    choiceFile = loopQuestionCaseSensitiveWithoutChecks('Quale file desideri utilizzare?')
    while(returnLoopResponse(lineIndexValues,choiceFile)):
        print('Hai inserito un valore non accettabile, riprova')
        choiceFile = functionAccettableValuesCaseSensitive(lineIndexValuesString)
        
    choiceFile = open(lines[int(choiceFile)-1].replace("\n",""),'r')
    diceNumber = []
    results = []
    axis = []
    measures = 0
    penalities = 0
    jsonString = choiceFile.read()
    jsonArray = json.loads(jsonString)
    print('Scelgo uno stato tra quelli disponibili nel file...')
    print()
    diceNumberOfJsonArray = throwDice(0,len(jsonArray)-1)
    guessResponse = 'no'
    guessResult = 'no'
    while (guessResponse == 'no' or guessResult == 'no'):
        choice = loopQuestion('Su quale asse vuoi eseguire la misurazione?',['x','y','z'])

        diceNumberWith20Faces = throwDice(1,20)
        diceNumber.append(diceNumberWith20Faces)
        axis.append(choice)
        
        if (diceNumberWith20Faces * 0.05) <= float(jsonArray[diceNumberOfJsonArray]['P'+choice.upper()]):
            results.append(1)

        else:
            results.append(-1)
       
        measures += 1
        print()
        tableUserResponse = loopQuestion('Vuoi visualizzare la tabella delle misurazioni attuali?',['si','no'])
        
        if tableUserResponse == 'si':
            
            print()
            
            for index in range(measures):
                print('Lancio Numero: '+str((index+1))+' | Asse di misura: '+str(axis[index])+' | Esito del lancio del dado: '+str(diceNumber[index])+' | '+'Esito Misura: '+str(results[index]))
        
        print()
        guessResponse = loopQuestion('Vuoi provare ad indovinare lo stato?',['si','no'])
        
        if (guessResponse == 'si'):
            statesQuestion = 'Puoi scegliere tra i seguenti stati: '
            indexJsonArray = 0
            correctStatesArray = []
            for state in jsonArray:
                correctStatesArray.append(state["ID"])
                if indexJsonArray == len(jsonArray)-1:
                    statesQuestion += state["ID"]
                else:
                    statesQuestion += state["ID"]+", "
                indexJsonArray += 1
            print()
            print(statesQuestion)
            stateUser = input()
            while(returnLoopResponse(correctStatesArray,stateUser)):
                print()
                print('Hai inserito un valore non accettabile, riprova')
                print(statesQuestion)
                stateUser = input()
        
            if(stateUser == jsonArray[diceNumberOfJsonArray]["ID"]):
                print()
                print('Risposta corretta')
                score += measures + penalities
                print('Punteggio = ', score)
                guessResult = 'si'
                print()
                rematchResponse = loopQuestion('Vuoi iniziare una nuova partita? Il punteggio non verrà resettato',['si','no'])
        
            else:
                print()
                print('Risposta errata')
                time.sleep(1)
                print('Inizia una nuova misurazione...')
                print()
                time.sleep(0.5)
                penalities += 5
                guessResult = 'no'
        else:
            print()
    
    

    
    