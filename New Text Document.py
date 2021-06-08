#################################################
# Author      : M. Samir Butt
# Skole       : Gand VGS
# Årsprøve    : 2021
#################################################
import time
import os
import ctypes
import msvcrt
import subprocess

from ctypes import wintypes

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)

SW_MAXIMIZE = 3

kernel32.GetConsoleWindow.restype = wintypes.HWND
kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)

#################################################
#maximize_conole: Denne funksjonen vil strekke shell konsollen til hele skjermen
#Etter-Bruk     : fanen vill tilpasse seg skjemen sin størrelse
#################################################
def maximize_console(lines=None):
    fd = os.open('CONOUT$', os.O_RDWR)
    try:
        hCon = msvcrt.get_osfhandle(fd)
        max_size = kernel32.GetLargestConsoleWindowSize(hCon)
        if max_size.X == 0 and max_size.Y == 0:
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        os.close(fd)
    cols = max_size.X
    hWnd = kernel32.GetConsoleWindow()
    if cols and hWnd:
        if lines is None:
            lines = max_size.Y
        else:
            lines = max(min(lines, 9999), max_size.Y)
        subprocess.check_call('mode.com con cols={} lines={}'.format(
                                cols, lines))
        user32.ShowWindow(hWnd, SW_MAXIMIZE)


#################################################
#clear          : Denne funksjonen gjør konsollen klar ved å slette det gammel info
#Etter-Bruk     : Sletter alt på konsollen
#################################################
def clear():
        os.system("cls")

        
#################################################
#startInterface : startInterface er funksjon for bruker grensesnitt
#pre-condition  : input må være en string 1, 2, 3 eller 4.
#post-condition : Printe ut meny og retunere valget av brukeren
#################################################       
def startInterface():
        clear()
        print("""###############################################################################################################################################
____    ____  __    _______  _______ .__   __.  _______ .______       _______      ______  __  .______    __    __   _______ .______          #
\   \  /   / |  |  /  _____||   ____||  \ |  | |   ____||   _  \     |   ____|    /      ||  | |   _  \  |  |  |  | |   ____||   _  \         #
 \   \/   /  |  | |  |  __  |  |__   |   \|  | |  |__   |  |_)  |    |  |__      |  ,----'|  | |  |_)  | |  |__|  | |  |__   |  |_)  |        #
  \      /   |  | |  | |_ | |   __|  |  . `  | |   __|  |      /     |   __|     |  |     |  | |   ___/  |   __   | |   __|  |      /         #
   \    /    |  | |  |__| | |  |____ |  |\   | |  |____ |  |\  \----.|  |____    |  `----.|  | |  |      |  |  |  | |  |____ |  |\  \----.    #
    \__/     |__|  \______| |_______||__| \__| |_______|| _| `._____||_______|    \______||__| | _|      |__|  |__| |_______|| _| `._____|    #
                                                                                                                                              #
                           .______   ____    ____         _______.     ___      .___  ___.  __  .______                                       #
                           |   _  \  \   \  /   /        /       |    /   \     |   \/   | |  | |   _  \                                      # 
                           |  |_)  |  \   \/   /        |   (----`   /  ^  \    |  \  /  | |  | |  |_)  |                                     # 
                           |   _  <    \_    _/          \   \      /  /_\  \   |  |\/|  | |  | |      /                                      #
                           |  |_)  |     |  |        .----)   |    /  _____  \  |  |  |  | |  | |  |\  \----.                                 #
                           |______/      |__|        |_______/    /__/     \__\ |__|  |__| |__| | _| `._____|                                 # """)                            
        print('###############################################################################################################################################')                                                  
        print('################################################################################################################################')
        print('#                                                                                                                              #')
        print('#      Vigenere                                                                                                                #')
        print('#      Cipher                                                                                                                  #')
        print('#      Enigma                                                                                                                  #')
        print('#      Maskin                                                                                By Samir                          #')
        print('#                                                                                                                              #')
        print('################################################################################################################################')
        print('       1.Krypter                                         #')
        print('       2.Dekrypt                                         #')
        print('       3.Krypter fra ukryptert.txt til kryptert.txt      #')
        print('       4.Exit                                            #')
        choice = input('Tast in et av valgene (1/2/3/4):')
        print ('###########################################################')
        return choice


alphabet = "abcdefghijklmnopqrstuvwxyz "

letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def encrypt(message, key):
    encrypted = ""
    split_message = [
        message[i : i + len(key)] for i in range(0, len(message), len(key))
    ]

    for each_split in split_message:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] + letter_to_index[key[i]]) % len(alphabet)
            encrypted += index_to_letter[number]
            i += 1

    return encrypted


def decrypt(cipher, key):
    decrypted = ""
    split_encrypted = [
        cipher[i : i + len(key)] for i in range(0, len(cipher), len(key))
    ]

    for each_split in split_encrypted:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] - letter_to_index[key[i]]) % len(alphabet)
            decrypted += index_to_letter[number]
            i += 1

    return decrypted

#################################################
#main : main funksjonen er hoved koden som styrer programmet
#pre-condition  : tar imot input
#post-condition : behandler input med funksjoner
#################################################       
def main():
    maximize_console() #fremkaller funksjon til å maksimere viduet
    # input fra bruker
    choice = startInterface() #starter consoll ui og tar i mot verdier fra meny til main

    if choice == "1":
        message = input("Hva vil du encryptere?") 
        keyword = input('Hva skal enkrypterings nøkkelen være?')

        encrypted = encrypt(message, keyword) 
        print("Etter enkryptering av " + message + " og nøkkelen " + keyword + " blir teksten til " + encrypted)
        time.sleep(3)

    elif choice == "2":
        message = input("Hva vil du decryptere?") 
        keyword = input('Hva skal enkrypterings nøkkelen være?')

        unencrypted = decrypt(message, keyword) 
        print("Etter dekryptering av " + message + " og nøkkelen " + keyword + " blir plainteksten " + unencrypted)
        time.sleep(3)

    elif choice == "3":
        f = open('ukryptert.txt', 'r')
        s = open('kryptert.txt' , 'w')
        
        print("Nå vil progammet ta et plaintekst fra ukryptert.txt og kryptere den med en nøkkel du velger")
        
        message = f.read()
        keyword = input("Skriv in hva nøkkel du ønsker:")

        encrypted = vigenere_decode(message, keyword)
        #if encrypted != alphabet
        print("Etter dekryptering av " + message + " og nøkkelen " + keyword + " blir plainteksten " + encrypted)
        s.write(encrypted)
        s.close()
        f.close()
        time.sleep(3)

    elif choice == "4":
        print("Prorgammet termineres. Hade godt!.")
        time.sleep(3)
        exit()
    
    else:
        print("Feilmelding. Skriv in Enten 1 eller 2 ")
        time.sleep(2)
        main()

    while True:
        #her er loopen som skal spørre om bruker å restarte eller ikke
        restart = str(input("Vil du starte programmet på nytt?")).lower()

        if restart == "yes" or restart == "y" or restart == 'ja' or restart == 'j':
            main() # restarter programmet

        elif restart == "n" or restart == "no" or restart == 'nei':
            print ("Prorgammet termineres. Hade godt!.")
            time.sleep(3)
            exit() #lukker programmet

        else:
            print('Feilmelding. Ja eller nei?')

#################################################
#main() : main() starter programmet
#pre-condition  : Start program
#post-condition : start main funtion
#################################################       
main()