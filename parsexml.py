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
# Python 3.8.2
from __future__ import annotations
import datetime 
import re

from variables import XML_PROD_FILEPATH, XML_TESTING_FILEPATH, GENERATED_HTML_FILEPATH, OPENING_TAGS, CLOSING_TAGS


def format_date(date_line) -> tuple[str, str]:
    date_and_time = re.match(r"(^<pubDate>)(.+?)(<\/pubDate>)", date_line).group(2)
    dt = datetime.datetime.strptime(date_and_time, '%Y-%m-%dT%H:%M:%S')
    date = "<p class=\"date\">" + dt.strftime("%A, %d %B %Y") + "</p>\n"
    time = dt.strftime("%H:%M")
    author_and_time = f"<p class=\"time\">{time}, never.easy</p>\n"
    return date, author_and_time

def format_content(content_line) -> str:
    if re.match(r"^<content:encoded>", content_line):
        content = re.match(r"(^<content:encoded><!\[CDATA\[)(.+)", content_line).group(2)
    elif re.match(r"(^.+?)(]]><\/content:encoded>$)", content_line):
        content = re.match(r"(^.+?)(]]><\/content:encoded>$)", content_line).group(1)
    else:
        content = content_line
    return content

def format_title(title_line) -> str: 
    title = "<h2>" + re.match(r"(^<title>)(.+?)(<\/title>)", title_line).group(2) + "</h2>"
    return title

# function to segregate raw_lines into separate items
def segregate_lines_into_items(arr) -> tuple[list, int]:
    sublists_counter = 0

    # temporary variables for storing content of each sublist
    sublist = [] 
    title_string = ""
    content_string = "" # this will have all lines of content appended
    item_date = ""
    item_signature = ""

    for thing in arr:
        thing = thing.lstrip()
        if thing != "</item>\n":
            if re.match(r"^<item>", thing):
                print("found an item")
            elif re.match(r"^<title>", thing):
                # TODO: format title
                title_string += format_title(thing)
            elif re.match(r"(^<pubDate>)(.+?)(<\/pubDate>)", thing):
                # TODO: format date and time strings
                item_date, item_signature = format_date(thing)
            elif re.match(r"^<content:encoded>", thing):
                # first line of content
                content_string = format_content(thing)
            else:
                content_string += format_content(thing)
        else: 
            # loop found item closing tag
            # add everything collected so far to the final list
            sublists_counter += 1
            sublist = [item_date, title_string, content_string, item_signature]
            list_of_items.append(sublist)
            # clear temp data
            sublist = []
            content_string = ""
            item_date = ""
            item_signature = ""
            title_string = ""
            print("Finished item no. %d" % (sublists_counter))
    
    return list_of_items, sublists_counter

testing = True

if testing: 
    file_to_parse = XML_TESTING_FILEPATH
else:
    file_to_parse = XML_PROD_FILEPATH

with open(file_to_parse, "r", encoding="utf-8", errors="strict") as lst:
    raw_items = lst.readlines()

# Loop for yeeting empty lines, single linebreaks or not needed tags
pattern = r"(^<wp:status>.+)|(^<wp:post_type>.+)|(^<category.+)|(^<excerpt:encoded>.+)|(^<description>.+)|(^<wp:post_date_gmt>.+)"
for i in raw_items: 
    if re.match(pattern, i.lstrip()) is not None or i == "\n" or i == '':    
        index_of_i = raw_items.index(i)
        trash = raw_items.pop(index_of_i)  # I realised this means one index number will be skipped aaaaaa TODO: rewrite this with append not-trash instead of pop trash
        print(f"trash was {trash} and is now gone")

# outcome needs to be nested list (list of lists), where each nested list is a single blog item
list_of_items = []
# list_o_items = [['item title', 'item content', 'item date', 'item signature'], ['item title', 'item content', 'item date', 'item signature'], ...]
# list_of_items = [sublist, sublist, sublist, ...]  

list_of_items, sublists_counter = segregate_lines_into_items(raw_items)
print(f"Did total of {sublists_counter} items, and the list of items has length of {list_of_items.__len__()}")

# TODO: reverse list_of_items so it starts with the earliest post
# TODO: only need posts from Novemver 2013 onwards

# With all items sorted in list_of_items, write them to a new html file
# imported variables contain all the HTML code needed around the content to display and print properly
with open(GENERATED_HTML_FILEPATH, "w", encoding="utf-8", errors="strict") as f:
    f.write(OPENING_TAGS)
    for each in list_of_items: 
        for i in each: 
            f.write(i)

    f.write(CLOSING_TAGS)
