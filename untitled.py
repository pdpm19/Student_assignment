import time
import random
random.uniform(9.5, 20)

####################################################################################################################################
# Classes
class Student:
    def __init__(self, id, mark, places):
        self.id = id
        self.mark = mark
        self.places = places
        self.assigned = 0

class University:
    def __init__(self, id, vacancies):
        self.id = id
        self.vacancies = vacancies

####################################################################################################################################
# Generators
def gen_mark(min, max):
    s = random.uniform(min, max)
    return float("{:.2f}".format(s))

def gen_options(n_universities, n_options):
    options = []
    for i in range(n_options):
        option = random.randint(1, n_universities)
        while(option in options):
            option = random.randint(1, n_universities)
        options.append(option)
    return options

def gen_students(n_students, n_universities):
    students = []
    for i in range(n_students):
        students.append(Student('S' + str(i+1), gen_mark(9.5, 20), gen_options(n_universities, random.randint(1,3))))
    return students

def gen_vacancies(n_min, n_max):
    return random.randint(n_min, n_max)

def gen_universities(n_universities):
    universities = []
    for i in range(n_universities):
        universities.append(University('U' + str(i+1), gen_vacancies(1, 1000)))
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
                    minor.append((student.id, student.mark))
                    break
    # (StudentID, Mark) and we want to sort by mark
    minor = sort_tuple_by_second_element(minor)[0]
    for student in students:
        if minor[0] == str(student.id):
            return student
    
####################################################################################################################################
# One-vs-All
def one_vs_all(students, universities, option, assigned, assigments):
    print('opção:', option)
    for student in students:
        # Only runs the unsigned students
        if student.assigned == 0:
            try:
                places = student.places
                universityID = places[option]
        
                # get university_info
                for i in universities:
                    if 'U' + str(universityID) == i.id:
                        university = i

                # university with vacancies
                if university.vacancies > 0:
                    assigments.append((student.id, university.id))
                    assigned.append(student.id)
                    university.vacancies -= 1
                    student.assigned = 1

                # university has no free vacancies
                else:
                    # get minor mark assigned to that university
                    minorStudent = get_minor_student(assigments, university.id, students)
                    if student.mark > minorStudent.mark:
                        assigments.remove((minorStudent.id, university.id))
                        assigned.remove(minorStudent.id)
                        minorStudent.assigned = 0

                        assigments.append((student.id, university.id))
                        assigned.append(student.id)
                        student.assigned = 1
            except:
                pass
####################################################################################################################################
# Main function
def main():
    '''
        This function does the following steps:
            1. Gets students and universities
            2. Displays the information for debugging
            3. Creates some auxiliary variables
            4. Runs the loop
            5. Displays the output for debugging
    '''
    # 1
    n_universities = 20
    n_students = 10000
    u = gen_universities(n_universities)
    s = gen_students(n_students, n_universities)
    
    '''
    # 2
    print('Students (id, mark, places):')
    for obj in s:
        print(obj.id, obj.mark, obj.places, sep=' ')
    
    print('\nUniversities (id, vacancies):')
    for obj in u:
        print(obj.id, obj.vacancies, sep=' ')
    '''
    # 3
    vacancies = 0
    option = 0
    assigned = []
    assigments = []
    max_options = 0
    all_assigned = True
    for student in s:
        if len(student.places) > max_options:
            max_options = len(student.places)
     # Gets the total vacancies
    for university in u:
        vacancies += university.vacancies
    students = s
    iter = 0
    
    # 4
    t0 = time.process_time()
    while True:
        '''
        # This loop does the following (numerated with the function comments)

            4.1. Checks if there is at least one student not assigned
            4.2. If all vacancies are occupied OR we reached the max option OR all students are assigned
                4.2.1. We do the final one vs all
            4.3. We do the n-option one vs all
        '''
        # 4.1
        for student in s:
            if student.assigned == 0:
                all_assigned = False
                break
        # 4.2
        if len(assigned) == vacancies or option >= max_options or all_assigned == True:
            #print('-----------------------------------------')
            #print('Iter:', iter)
            # Run last time
            unsigned = one_vs_all(students, u, option, assigned, assigments)
            #print('-----------------------------------------')
            break
        # 4.3
        else:
            #print('-----------------------------------------')
            #print('Iter:', iter)
            unsigned = one_vs_all(students, u, option, assigned, assigments)
        iter += 1
        option += 1
        all_assigned = True
    t1 = time.process_time()  
    # 5
    print('Assigned:', assigned)
    print('Assigments:', assigments)
    print(f"Elapsed time = {t1-t0}s")

main()


import csv
# Tests
def test():
    students = []
    universities = []

    students.append(Student('S1', 16.38, [1,3]))
    students.append(Student('S2', 12.24, [4,3]))
    students.append(Student('S3', 12.3, [1,2,5]))
    students.append(Student('S4', 11.54, [2,5,4]))
    students.append(Student('S5', 17.4, [4,3,1]))
    students.append(Student('S6', 9.59, [3]))
    students.append(Student('S7', 12.17, [3,2,5]))
    students.append(Student('S8', 9.55, [1]))
    students.append(Student('S9', 19.73, [1,5,3]))
    students.append(Student('S10', 15.83, [2,3]))
    
    
    with open('uni.csv', 'r') as csvfile:
        spam = csv.reader(csvfile, delimiter=';')
        for row in spam:
            s = University(row[0], int(row[1]))
            universities.append(s)
    
    # faz a magia de correr a main
    # 2
    print('Students (id, mark, places):')
    for obj in students:
        print(obj.id, obj.mark, obj.places, sep=' ')
    
    print('\nUniversities (id, vacancies):')
    for obj in universities:
        print(obj.id, obj.vacancies, sep=' ')
    
    # 3
    vacancies = 0
    option = 0
    assigned = []
    assigments = []
    max_options = 0
    all_assigned = True
    for student in students:
        if len(student.places) > max_options:
            max_options = len(student.places)
     # Gets the total vacancies
    for university in universities:
        vacancies += university.vacancies
    iter = 0
    
    # 4
    while True:
        '''
        # This loop does the following (numerated with the function comments)

            4.1. Checks if there is at least one student not assigned
            4.2. If all vacancies are occupied OR we reached the max option OR all students are assigned
                4.2.1. We do the final one vs all
            4.3. We do the n-option one vs all
        '''
        # 4.1
        for student in students:
            if student.assigned == 0:
                all_assigned = False
                break
        # 4.2
        if len(assigned) == vacancies or option >= max_options or all_assigned == True:
            print('-----------------------------------------')
            print('Iter:', iter)
            # Run last time
            unsigned = one_vs_all(students, universities, option, assigned, assigments)
            print('-----------------------------------------')
            break
        # 4.3
        else:
            print('-----------------------------------------')
            print('Iter:', iter)
            unsigned = one_vs_all(students, universities, option, assigned, assigments)
        iter += 1
        option += 1
        all_assigned = True
        
    # 5
    print('Assigned:', assigned)

# test()