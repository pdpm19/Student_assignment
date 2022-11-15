from functions_repo import *
from debug import *
import time

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
    # n_universities >= n_options, else it's not gonna work
    n_universities = 500
    min_vacancies = 1
    max_vacancies = 300
    n_students = 10000
    max_options = 3
    universities = gen_universities(n_universities, min_vacancies, max_vacancies)
    students = gen_students(n_students, max_options, n_universities)
    
    # Usa o exemplo criado antes
    universities = read_universities()
    students = read_students()
    
    # 2
    display(students, universities)
    
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
    unsigned = students.copy()
    lastUnsigned = []
    
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
        for student in students:
            if student.assigned == False:
                all_assigned = False
                break
        # 4.2
        if all_assigned == True or unsigned == lastUnsigned:
            lastUnsigned = unsigned.copy()
            print('-----------------------------------------')
            print('Last Iter:', iter)
            # Run last time
            unsigned = one_vs_all(students, universities, option, assigned, assigments)
            print('-----------------------------------------')
            break
        # 4.3
        else:
            print('-----------------------------------------')
            print('Iter:', iter)
            lastUnsigned = unsigned.copy()
            unsigned = one_vs_all(students, universities, option, assigned, assigments)
        iter += 1
        option += 1
        all_assigned = True
    t1 = time.process_time()  
    # 5
    print('Assigned:', assigned)
    print('Assigments:', assigments)
    print('Percentagem:', len(assigned)/len(students))
    print(f"Elapsed time = {t1-t0}s")

main()