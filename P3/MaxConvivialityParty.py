import random

class Employee(object):
    def __init__(self, value, subordinates):
        self.value = value
        self.subordinates = subordinates
        
def create_orgchart(number_stuff, max_subordinates):
    ids = range(number_stuff)
    #shuffle
    for id_index in xrange(number_stuff - 1):
        swap_index = random.randint(id_index, number_stuff - 1)
        buffer_ = ids[swap_index]
        ids[swap_index] = ids[id_index]
        ids[id_index] = buffer_ 
        
    id_last_with_boss = 0
    orgchart = {}
    for id_assign_subordinates in ids:
        num_subordinates = random.randint(1, max_subordinates) #can be > number_stuff, it is ok
        subordinates = ids[id_last_with_boss + 1 : 
                           id_last_with_boss + num_subordinates + 1]
        orgchart[id_assign_subordinates] = Employee(value = random.random(), 
                                                       subordinates = subordinates)
        id_last_with_boss += num_subordinates
    
    return orgchart, ids[0]


def find_max_convivality_party(employees, key_boss):
    
    # assign level for each employee
    employee_levels = [[key_boss]]
    while True:
        new_level = []
        for employee_nb in employee_levels[0]:
            assert employee_nb in employees.keys()
            new_level += employees[employee_nb].subordinates
        if new_level:
            employee_levels = [new_level] + employee_levels
        else:
            break
        
    # do dynamic programming per level        
    number_invite_not_invite = {}        
    for level in employee_levels:
        for employee in level:
            accumul_invite_subordonates = 0.
            accumul_not_invite_subordonates = 0.
            for subordinate in employees[employee].subordinates:
                accumul_invite_subordonates += number_invite_not_invite[subordinate][0]
                accumul_not_invite_subordonates += number_invite_not_invite[subordinate][1]
            number_invite_not_invite[employee] = \
                (employees[employee].value + accumul_not_invite_subordonates, accumul_invite_subordonates)
    
    if number_invite_not_invite[key_boss][0] > number_invite_not_invite[key_boss][1]:
        return "invite boss", number_invite_not_invite[key_boss][0], number_invite_not_invite
    else:
        return "not invite boss", number_invite_not_invite[key_boss][1], number_invite_not_invite 
    
if __name__ == '__main__':
    employees, key_boss = create_orgchart(number_stuff = 5, max_subordinates = 2)
    print "boss", key_boss
    for key, value in employees.iteritems():
        print key, value.value, value.subordinates
    msg, total_value, details = find_max_convivality_party(employees = employees, key_boss = key_boss)
    print msg, total_value
    for key, detail in details.iteritems():
        print key, detail