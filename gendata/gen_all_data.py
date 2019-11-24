import codecs
import uuid
import json
import os
from utilities import *

#####################################
# config variable

db_name = "btlhqt"
classdb_insert =  "INSERT INTO `courses` (`idcourse`, `course_code`, `course_name`) VALUES "
studentdb_insert= "INSERT INTO `students` (`idstudent`, `name`, `dob`) VALUES "
registrationdb_insert = "INSERT INTO `registrations` (`idstudent`, `idcourse`) VALUES "

number_row_classes = 25000000
number_row_students = 25000000
number_row_registrations = 50000000
number_split_sql = 5000

directory = "./data/"
path_classes = f"{directory}courses.csv"
path_students = f"{directory}students.csv"
path_registration  = f"{directory}registrations.csv"
path_registration_sql  = f"{directory}registrations.sql"
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

remove_file(path_registration_sql)
write_append_data(path_registration_sql, "DROP DATABASE IF EXISTS btlhqt;")
write_append_data(path_registration_sql, "CREATE DATABASE btlhqt;")
write_append_data(path_registration_sql, "USE btlhqt;")
write_append_data(path_registration_sql, 
"""CREATE TABLE courses (
idcourse VARCHAR(200) PRIMARY KEY ,
course_code VARCHAR(200) NOT NULL ,
course_name VARCHAR(200) NOT NULL 
);
""")
write_append_data(path_registration_sql, 
"""CREATE TABLE students (
idstudent VARCHAR(200) PRIMARY KEY ,
name VARCHAR(200) NOT NULL ,
dob DATETIME NOT NULL 
) ;
""")
write_append_data(path_registration_sql, 
"""CREATE TABLE registrations (
idstudent VARCHAR(200) NOT NULL ,
idcourse VARCHAR(200) NOT NULL 
) ;
""")


write_append_data(path_registration_sql, 
"""ALTER TABLE courses MODIFY course_name VARCHAR(200) CHARACTER SET utf8;
ALTER TABLE students MODIFY name VARCHAR(200) CHARACTER SET utf8;

""")

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
            
            if(idx % number_split_sql == 0):
                write_append_data(path_registration_sql, classdb_insert)
            if(idx % number_split_sql == number_split_sql - 1):
                write_append_data(path_registration_sql, f"('{id}','{class_split[0]} {i+1}','{class_split[1]}');")
            else:
                if(class_ == classes_[len(classes_) - 1] and i == (int(number_row_classes/len(classes_)))):
                    write_append_data(path_registration_sql, f"('{id}','{class_split[0]} {i+1}','{class_split[1]}');")
                else:
                    write_append_data(path_registration_sql, f"('{id}','{class_split[0]} {i+1}','{class_split[1]}'),")

            idx += 1
            if(idx % number_log == 0):
                log_helper("course", idx, number_row_classes, number_log)

####################################
# Gen data mysql for student table from names.txt
####################################
if write_students:
    remove_file(path_students)
    remove_file(path_id_students)

    for i in range(number_row_students):
        id = str(uuid.uuid4())
        name = get_random_name()
        dob = str(random1995To2001())
        data = f"{id},{name},{dob}"
        write_append_data(path_students, data)
        write_append_data(path_id_students, id)
        if(i % number_split_sql == 0):
            write_append_data(path_registration_sql, studentdb_insert)
        if(i % number_split_sql == number_split_sql - 1):
            write_append_data(path_registration_sql, f"('{id}','{name}','{dob}');")
        else:
            write_append_data(path_registration_sql, f"('{id}','{name}','{dob}'),")

        if(i % number_log == 0):
            log_helper("student", i, number_row_students, number_log)

###################################
# Gen data mysql for registration table
###################################

if write_registration:
    remove_file(path_monggo)
    remove_file(path_registration)
    # remove_file(path_registration_sql)

    
    
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
            
            if(idx % number_split_sql == 0):
                write_append_data(path_registration_sql, registrationdb_insert)
            if(idx % number_split_sql == number_split_sql - 1):
                write_append_data(path_registration_sql, f"('{idstudent}','{idclass}');")
            else:
                write_append_data(path_registration_sql, f"('{idstudent}','{idclass}'),")
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
