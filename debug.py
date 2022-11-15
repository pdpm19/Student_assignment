from functions_repo import *

# Debug/Test functions
def debug_creation():
    n_students = 100
    n_options = random.randint(1,6)
    
    # n_universities >= n_options
    n_universities = 6
    min_vacancies = 10
    max_vacancies = 1000
    
    #students = gen_students(n_students, n_options, n_universities)
    #universities = gen_universities(n_universities, min_vacancies, max_vacancies)
    
    display(students, universities)
    
# Debug reading
def debug_reading():
    students = read_students()
    universities = read_universities()
    
    display(students, universities)
    

def debug_writing(students, universities):
    write_students(students)
    
####################################################################################################################################
def display(students, universities):
    print('Display Students\n---')
    for i in students:
        print(i.id, i.places, i.assigned, sep=';')
        print('---')
    print('\nDisplay Universities\n***')
    for i in universities:
        print(i.id, i.vacancies, sep=';')
        print('***')
        
'''
students = gen_students(100,6,10)
debug_writing(students, [])
debug_reading()
'''