
def check_quiz_solution(what_are_we_looking_for, correct_solution, solution_units = None, tolerance = 0.0001):
    question = "What is " + what_are_we_looking_for                  # put together the quesion
    if (solution_units is not None) and (solution_units != ""):
        solution_units_to_use = " " + solution_units
        question += " (in " + solution_units + ")"
    else: 
        solution_units_to_use = ""
    user_solution_string = input(question + "?")

    try:                                                             # if the solution is a the right format
        correct = False
        if isinstance(correct_solution, str):
            if correct_solution == user_solution_string:
                correct = True
        else:
            user_solution_number = float(user_solution_string)
            if abs(user_solution_number - correct_solution) < tolerance: # if it is very close to the correct number
                correct = True

        if correct:
            conclusion = "This is correct, congratulations!"         # then congratulations
        else:
            conclusion = "Unfortunately this is incorrect."          # otherwise better luck next time
    except:
        if (user_solution_string == ""):
            conclusion = "You are not even trying!"                  # if the solution is empty, show an error msg
            user_solution_string = "empty"
        else:
            conclusion = "This is not a number!"                     # if the solution was not a number, show an error msg
    return (what_are_we_looking_for + " is " + str(correct_solution) + solution_units_to_use,
            "Your solution is " + user_solution_string + solution_units_to_use, 
            conclusion)
