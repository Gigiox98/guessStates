from pathlib import Path
import math
import os

def insertInput(question):
    print(question)
    value = input()
    print()
    return value;

userPathHome = str(Path.home()).replace("\\","/")
print('Inserisci il nome del file che desideri creare, senza l\'estensione')
file_name = input()
print()
absolute_path = userPathHome+"/"+file_name+".txt"

print('Quanti stati desideri inserire?')
try :
    numberOfStates = int(input())
    if(numberOfStates > 0):
        print()
        indexOfState = 0
        tableText = 'ID\tx\ty\tz\tPX\tPY\tPZ\n'
        jsonText = '[\n'
        while(indexOfState < numberOfStates):
            jsonText += '\t{\n\t\t'
            id = insertInput('Inserisci l\'ID')
            teta = float(insertInput('Inserisci il valore dell\'angolo teta'))
            phi = float(insertInput('Inserisci il valore dell\'angolo phi'))
            x = round(math.sin(math.radians(teta))* math.cos(math.radians(phi)),2)
            y = round(math.sin(math.radians(teta))* math.sin(math.radians(phi)),2)
            z = round(math.cos(math.radians(teta)),2)
            jsonText += '\"ID\":'+'\"'+ id +'\",\n\t\t'
            jsonText += '\"x\":'+'\"'+ str(x) +'\",\n\t\t'
            jsonText += '\"y\":'+'\"'+ str(y) +'\",\n\t\t'
            jsonText += '\"z\":'+'\"'+ str(z) +'\",\n\t\t'
            jsonText += '\"PX\":'+'\"'+ str(round(0.5*(1+x),2)) +'\",\n\t\t'
            jsonText += '\"PY\":'+'\"'+ str(round(0.5*(1+y),2)) +'\",\n\t\t'
            jsonText += '\"PZ\":'+'\"'+ str(round(0.5*(1+z),2)) +'\"\n\t'
            jsonText += '}'
            tableText += id+'\t'+str(x)+'\t'+str(y)+'\t'+str(z)+'\t'+str(round(0.5*(1+x),2))+'\t'+str(round(0.5*(1+y),2))+'\t'+str(round(0.5*(1+z),2))+'\n'
            
            if indexOfState < numberOfStates-1:
                jsonText += ',\n'
            else:
                jsonText += '\n]'
            
            indexOfState += 1
            
            print('Lo stato numero '+str(indexOfState)+' con ID '+ id +' è stato generato correttamente.')
            print()
        
        insertFile = True
        if os.path.exists(userPathHome+"/"+file_name+".txt"):
            insertFile = False
            
        newFileJson = open(userPathHome+"/"+file_name+".txt", 'w')
        newFileJson.write(jsonText)
        newFileJson.close()
        
        newFileJson = open(userPathHome+"/"+file_name+"_table.txt", 'w')
        newFileJson.write(tableText)
        newFileJson.close()
        
        if insertFile:
            if not os.path.exists(userPathHome+'/pathsJson.txt'):
                filePaths = open(userPathHome+'/pathsJson.txt', 'w')
                filePaths.write(absolute_path+"\n")
                filePaths.close()
            else:
                filePaths = open(userPathHome+'/pathsJson.txt', 'a')
                filePaths.write(absolute_path+"\n")
                filePaths.close()
            
        print('Struttura creata correttamente')
        os.system('start '+userPathHome+"/"+file_name+"_table.txt")
    else:
        print('Input non coerente')
except:
    print('Input non coerente')