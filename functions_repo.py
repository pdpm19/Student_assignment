'''
Students:
    int            = student_id
    list of tuples = (university_id, mark1),(university_id, mark2)
    bool           = assigned

Universities:
    int            = university_id
    int            = vacancies

E.g:
[S1, [(U1, 16), (U2, 15)]]
[S2, [(U2, 18), (U1, 10)]]

[U1, 100]
[U2, 75]
'''

# Imports
import time
import random
import csv
import sys
import os
####################################################################################################################################
# Classes
class Student:
    def __init__(self, id, places, assigned):
        self.id = id
        self.places = places
        self.assigned = assigned

class University:
    def __init__(self, id, vacancies):
        self.id = id
        self.vacancies = vacancies

####################################################################################################################################
# Generators
def gen_mark(min, max):
    s = random.uniform(min, max)
    return float("{:.2f}".format(s))

def check_duplicated(option, options, i, n_universities):
    # 1st stopping condition
    if i == len(options):
        return option
    else:
        op2 = options[i]
        # 2nd if they are equal, generate new and start the process
        if option[0] == op2[0]:
            mark = gen_mark(9.5, 20)
            option = ('U' + str(random.randint(1, n_universities)), mark)
            return check_duplicated(option, options, 0, n_universities)
        else:
            # 3rd moves to the next position
            return check_duplicated(option, options, i+1, n_universities)  

def gen_options(n_universities, n_options, options):
    for i in range(n_options):
        mark = gen_mark(9.5, 20)
        option = ('U' + str(random.randint(1, n_universities)), mark)
        if options != []:
            option = check_duplicated(option, options, 0,n_universities)
        options.append(option)
    return options

def gen_students(n_students, n_options, n_universities):
    students = []
    options = []
    for i in range(n_students):
        options = gen_options(n_universities, n_options, options)
        student = Student('S' + str(i+1), options, False)
        students.append(student)
        options = []
    return students

def gen_universities(n_universities, min_vacancies, max_vacancies):
    universities = []
    for i in range(n_universities):
        uni = University('U' + str(i+1), random.randint(min_vacancies, max_vacancies))
        universities.append(uni)
    return universities

####################################################################################################################################
# Get lowest mark student from assigned list
def sort_tuple_by_second_element(tuple):
    tuple.sort(key = lambda x:x[1])
    return tuple

# Return the students in atrib:
def get_minor_student(atrib, universityID, students):
    minor = []
    for i in atrib:
        if universityID == i[1]:
            for student in students:
                if i[0] == student.id:
                    minor.append((student.id, i[2]))
                    break
    # (StudentID, Mark) and we want to sort by mark
    minor = sort_tuple_by_second_element(minor)[0]
    #print('Minor será', minor)
    return minor
    for student in students:
        if minor[0] == str(student.id):
            return student
    
####################################################################################################################################
# One-vs-All
def one_vs_all(students, universities, option, assigned, assigments):
    unsigned = []
    for student in students:
        # Only runs the unsigned students
        if student.assigned == False:
            try:
                places = student.places
                university = places[option]
                universityID = university[0]
                studentMark = university[1]
                #print(universityID, studentMark)
                # get university_info
                for i in universities:
                    if universityID == i.id:
                        university = i

                # university with vacancies
                if university.vacancies > 0:
                    assigments.append((student.id, university.id, studentMark))
                    assigned.append(student.id)
                    university.vacancies -= 1
                    student.assigned = True

                # university has no free vacancies
                else:
                    #print('Ass', assigments)
                    # get minor mark assigned to that university
                    minorStudent = get_minor_student(assigments, university.id, students)
                    #print(studentMark, minorStudent[1])
                    if studentMark > minorStudent[1]:
                        assigments.remove((minorStudent[0], university.id, minorStudent[1]))
                        assigned.remove(minorStudent[0])
                        for i in students:
                            if minorStudent[0] == i.id:
                                i.assigned = False
                                break
                        
                        assigments.append((student.id, university.id, studentMark))
                        assigned.append(student.id)
                        student.assigned = True
            except:
                pass
    print(assigments)
    for i in students:
        if i.assigned == False:
            unsigned.append(i)
    return unsigned
####################################################################################################################################
# Read Files
def read_students():
    students = []
    path = os.getcwd()
    with open(os.path.join(path, 'db/studentsC.csv')) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            places = []
            # deals with the list of tuples
            aux = row[1]
            aux = aux.split('), (')
            aux_final = []
            for i in range(len(aux)):
                if i == 0:
                    aux_final.append(aux[i][2:])
                elif i == len(aux)-1:
                    aux_final.append(aux[i][:len(aux[i])-2])
                else:
                    aux_final.append(aux[i])
            places = []
            for j in range(len(aux_final)):
                aux = aux_final[j].split(',')
                universityID = str(aux[0][1:len(aux[0])-1])
                mark = float(aux[1][:])
                places.append((universityID, mark))
            if row[2] == 'False':
                row[2] = False
            else:
                row[2] = True
            students.append(Student(row[0], places, row[2]))
    return students

def read_universities():
    universities = []
    path = os.getcwd()
    with open(os.path.join(path, 'db/universities.csv')) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            universityID = str(row[0])
            universityVacancies = int(row[1])
            universities.append(University(universityID, universityVacancies))
    return universities

####################################################################################################################################
# Write Files
def write_students(students):
    header = ['ID', 'Options', 'Assigned']
    path = os.getcwd()
    with open(os.path.join(path, 'db/test.csv'), 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        #writer.writerow(header)
        data = []
        for i in students:
            data.append([i.id, i.places, i.assigned])
        print(data)
        writer.writerows(data)