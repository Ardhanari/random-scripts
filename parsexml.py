# parse xml file 
# save every item as 'item' in an array
# reverse array (first posted as [0], last posted as [n])
# write function that takes item -> rearranges the necessary elements so they look like that:

# <p class="date">{{weekday}}, {{dd MM YYYY}}</p>
# <h2>title</h2>
# {{content}} # it has <p> embedded already, needs to be stripped of <![CDATA
# {{HH:MM}}, never.easy

# store them all in a new array
# (or append to a long .html doc?) 

# the rest I can do in HTML/CSS if necessary

# ----

import re
from variables import XML_TESTING_FILEPATH

file_to_parse = XML_TESTING_FILEPATH # opens as a list HO

with open(file_to_parse, "r") as lst:
    array_of_items = lst.readlines()

# Loop for yeeting empty lines or single linebreaks 
for i in array_of_items: 
    if i == "\n" or i == '':
        index_of_i = array_of_items.index(i)
        trash = array_of_items.pop(index_of_i)
        print("trash is now gone")

print(array_of_items[0]) # check first item after deleting trash # tb deleted later

# outcome needs to be nested list (list of lists), where each nested list is a single blog item
list_of_items = []
# list_o_items = [['item title', 'item content', 'item date'], ['item title', 'item content', 'item date'], ...]
# list_of_items = [sublist, sublist, sublist, ...]

def clear_variables(): 
    print("VAPORIZE!")
    sublist = []
    content_string = ""
    item_date = ""
    title_string = ""
    

# attempt to segregate it into separate items
def segregate_lines_into_items(arr):
    sublist_counter = 0

    # temporary variables, cleared after each <item> with clear_variable()
    sublist = [] # TODO: check if python can do fixed size list?
    title_string = ""
    content_string = "" # this will have all lines of content appended
    item_date = ""

    for thing in arr:
        thing = thing.lstrip()
        if re.match(r"^<item>", thing):
            print("found an item")
        elif re.match(r"^<title>", thing):
            title_string += thing
        elif re.match(r"^<wp:post_date_gmt>", thing):
            item_date += thing
        elif re.match(r"^<content:encoded>", thing):
            # first line of content
            content_string += thing
        elif re.match(r"^</item>", thing):
            sublist_counter += 1
            clear_variables()
            print("Finished item no. %d" % (sublist_counter))
        else:
            content_string += thing

            # move to an inside loop to append all the lines 
            # till it's <item> again - then break
            # and repeat
        sublist = [title_string, content_string, item_date]
    
    return sublist, sublist_counter # TODO: return a final nested list instead (so insert each sublist into a list_of_items and then clear)

sublist, sublist_counter = segregate_lines_into_items(array_of_items)
print(f"Did total of {sublist_counter} items, and the list of items is: \n")
for each in list_of_items:
    print(each)