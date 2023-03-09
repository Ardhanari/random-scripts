"""
This code gets a response from a given url, searches through it to find an image and button to the next page using regex (consts RE_IMG_SRC and RE_NEXT_PAGE are regex pattern to isolate links to both).
Then saves an image to local drive (path given through SAVE_TO const) using save_to_drive(image_url) function - and, after a short sleep, continues to the next page to repeat the process. 
After there's no more 'next_page' link, loop breaks with IndexError trying to read from regex result list the link to next page when the list is of length 0. 
"""
from time import sleep
import requests, re, shutil
from os import path
from variables import PATH, RE_IMG_SRC, RE_NEXT_PAGE, SAVE_TO

def save_to_drive(img_to_save): 
    img_res = requests.get(img_to_save, stream = True)
    file_name = path.basename(img_res.url)

    if img_res.status_code == 200:
        with open(SAVE_TO + file_name,'wb') as f:
            shutil.copyfileobj(img_res.raw, f)
        print('Yay, strip saved: ',file_name)
    else:
        print('Couldn\'t save a strip :(\n Status code: ', str(img_res.status_code))

current_page = PATH

# begin the loop (will stop once there's no `next page`)
while True:

    # 1 - take url and return the content of the website
    stripfield_page = requests.get(current_page) # stripfield_page -> HTTP response / .text -> full code

    # 2 - find URL of img
    imgs_found = re.findall(RE_IMG_SRC, stripfield_page.text)

    # 3 - save img(s) to drive
    if len(imgs_found) > 1: 
        for i in range(len(imgs_found)):
            img_to_save = imgs_found[i][1]
            save_to_drive(img_to_save)
    else:
        img_to_save = imgs_found[0][1]
        save_to_drive(img_to_save)

    # 4 - find URL of next page 
    print(re.findall(RE_NEXT_PAGE, stripfield_page.text))
    next_page = re.findall(RE_NEXT_PAGE, stripfield_page.text)[0][0]
    current_page = next_page

    print("Going for a nap :)")
    # 5a - pretend you're human
    sleep(3)
    print("Woke up! Trying the next iteration...")
    # 5 - rinse and repeat