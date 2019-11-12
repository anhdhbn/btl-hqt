import codecs
import os
from random import randrange, randint
from datetime import timedelta
from datetime import datetime
import uuid
import codecs
import json
import time


def get_all_text_from_file_to_array(path):
    with codecs.open(path, 'r', encoding='utf8') as f:
        content = f.readlines()
        return [x.strip() for x in content]

cached_append = {}

def write_append_data(path, data):
    # print(cached_append.keys())
    if(path in cached_append.keys()):
        cached_append[path].write(f"{data}\n")
    else:
        cached_append[path] = codecs.open(path, 'a', encoding='utf8')
        cached_append[path].write(f"{data}\n")

def remove_file(path):
    try:
        os.remove(path)
    except OSError:
        pass

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    random_day = randrange(delta.days)
    return start + timedelta(days=random_day)

def random1995To2001():
    start = datetime(year=1995, month=1, day=1)
    end = datetime(year=2001, month=1, day=1)
    return random_date(start, end)

names = get_all_text_from_file_to_array("names.txt")

def get_random_name():
    length = len(names)
    idx = randrange(length - 1)
    return names[idx]

cached = {}

def read_at_line(path, line):
    if(path in cached.keys()):
        temp = cached[path].readline().strip()
        if(temp == ""):
            cached[path] = codecs.open(path, 'r', encoding='utf8')
            return cached[path].readline().strip()
        else:
            return temp
    else:
        cached[path] = codecs.open(path, 'r', encoding='utf8')
        return cached[path].readline().strip()
        # with codecs.open(path, 'r', encoding='utf8') as f:
        #     cached[path] = [x.strip() for x in f.readlines()]
        #     return cached[path][line]

def random_number(number):
    return randint(0, number)

last_time = time.time()

def log_helper(curent_obj, current_row, total_row, number_log):
    global last_time
    if last_time is not None:
        current_time = time.time()
        time_run = current_time - last_time
        last_time = current_time       
        estimated = (total_row - current_row)/number_log * time_run
        estimated  = time.strftime('%H:%M:%S', time.gmtime(estimated))
    else:
        last_time = time.time() 
        estimated = "None"
    percent  = round(current_row*100.0/total_row, 1)
    print(f"Writing {curent_obj}... {percent}% {current_row}/{total_row} Estimate: {estimated}")