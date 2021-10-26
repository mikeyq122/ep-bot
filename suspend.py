from pynput import keyboard



def wait_for_key(key):
    print("Waiting for key " + str(key))
    def on_press(input):
        pressed=str(input)

        if (key == pressed):
            return False


    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    print("Got key, resuming")
    return key
