# Requirements:

1. tkinter  
(pip install tk)

2. screeninfo  
(pip install screeninfo)

3. PIL  
(pip install Pillow)

4. lxml  
(pip install lxml)

You can get pip by running:

    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py

# Usage:
    python dvd_widget [ARGS]

        --button - bool - Adds buttons to top left corner of screen to add or remove logos, or quit/save and quit if --save is true.
        --auto   - bool - Enables autosave. (Autosaves once per minute)
        --save   - str  - Dir to save to.
        --load   - str  - Dir to load from.
        NOTE: Save directories are created in the saves directory. The save/load function does not need a path, just a name.

        --num    - int  - Number of dvd logos to make. (Only if load is not used, or load fails)
        --help   -        Shows help.


## Disclaimer:
This code only works on Windows due to how tkinter works.  
It is spaghetti code through and through.  
I am not responible for any damages to your mental state resulting from use of this code.  