import codecs
import uuid
import json
from utilities import *

#####################################
# config variable
number_row_classes = 25000000
number_row_students = 25000000
number_row_registrations = 50000000

directory = "./data/"
path_classes = f"{directory}courses.csv"
path_students = f"{directory}students.csv"
path_registration  = f"{directory}registrations.csv"
path_monggo  = f"{directory}mongo.json"

path_id_classes = f"{directory}idcourses.txt"
path_id_students = f"{directory}idstudents.txt"

write_classes = True
write_students = True
write_registration = True
number_log = 5000
#####################################


if not os.path.exists(directory):
    os.makedirs(directory)


#####################################
# Gen data mysql for classes table from classes.txt
#####################################
if write_classes:
    remove_file(path_classes)
    remove_file(path_id_classes)

    classes_ = get_all_text_from_file_to_array("classes.txt")

    idx = 0
    for class_ in classes_:
        for i in range(int(number_row_classes/len(classes_)) + 1):
            class_split = class_.split('|')
            id = str(uuid.uuid4())
            data = f"{id},{class_split[0]} {i+1},{class_split[1]}"
            write_append_data(path_classes, data)
            write_append_data(path_id_classes, id)
            
            idx += 1
            if(idx % number_log == 0):
                log_helper("course", idx, number_row_classes, number_log)

####################################
# Gen data mysql for student table from names.txt
####################################
if write_students:
    remove_file(path_students)
    remove_file(path_id_students)
    idx = 0
    for i in range(number_row_students):
        id = str(uuid.uuid4())
        data = f"{id},{get_random_name()},{str(random1995To2001())}"
        write_append_data(path_students, data)
        write_append_data(path_id_students, id)
        idx += 1
        if(idx % number_log == 0):
            log_helper("student", i, number_row_students, number_log)

###################################
# Gen data mysql for registration table
###################################

if write_registration:
    remove_file(path_monggo)
    remove_file(path_registration)

    write_append_data(path_monggo, "[")
    idx = 0
    for i in range(number_row_students):
        idstudent = read_at_line(path_id_students, i)
        infostudent = read_at_line(path_students, i).split(',')
        
        obj = {
                "name": infostudent[1],
                "dob": infostudent[2],
                "registrations": [
                    
                ]
            }

        for j in range(int(number_row_registrations/number_row_students)):
            number_line_class = random_number(number_row_classes)
            idclass  = read_at_line(path_id_classes, number_line_class)
            infoclass =  read_at_line(path_classes, number_line_class).split(',')
            data = f"{idstudent},{idclass}"
            write_append_data(path_registration, data)

            #########################
            #  data mongo
            #########################
            obj["registrations"].append({
                "course_code":  infoclass[1],
                "course_name" : infoclass[2]
            })
            idx += 1

        data_mongo = f"{json.dumps(obj,ensure_ascii=False)}"
        if(i != number_row_students - 1):
            data_mongo  += ","
        write_append_data(path_monggo, data_mongo)
        if(idx % number_log == 0):
            log_helper("registration", idx, number_row_registrations,  number_log)

    write_append_data(path_monggo, "]")