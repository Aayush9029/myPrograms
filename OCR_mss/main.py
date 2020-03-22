'''
Alto's adventure speeed tracker
Covid-code 
'''

import mss
import pytesseract
from numpy import array 

last_distance = 0
last_speed = 0
while True:
    with mss.mss() as sct:

        monitor = {"top": 30, "left": 585, "width": 120, "height": 30}
        img = sct.grab(monitor)
        img = array(img)
        raw_string = pytesseract.image_to_string(img)
        raw_string = (raw_string[:-1]).replace(",", "")
        raw_string = (raw_string).replace(".", "")
        if raw_string != "" and raw_string.isdigit:
            try:
                int_raw = int(raw_string)
                if last_distance != int_raw:
                    new_speeed = int_raw - last_distance
                    if last_speed != new_speeed:
                        print(new_speeed)
                        last_speed = new_speeed
                    last_distance = int_raw 

            except ValueError:
            #   print("value error", raw_string)
                pass
        else:
            pass
            # ("Print it's a string", raw_string)
