import numpy
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker as mticker
from datetime import datetime
import os

def check_quiz_solution(what_are_we_looking_for, correct_solution, solution_units = None, tolerance = 0.0001):
    question = "What is " + what_are_we_looking_for                  # put together the quesion
    if solution_units is not None:
        solution_units_to_use = " " + solution_units
        question += " (in " + solution_units + ")"
    else: 
        solution_units_to_use = ""
    user_solution_string = input(question + "?")

    try:                                                             # if the solution is a number
        user_solution_number = float(user_solution_string)
        if abs(user_solution_number - correct_solution) < tolerance: # if it is very close to the correct number
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

# this function returns the filename of the saved figure if we save it,
#            it returns None if we don't save it             
def plt_envelope(func_to_call, save_file = True, add_grid = False, solution_object = None, **kwargs):
    plt.close()

    fig = plt.figure(figsize = (5, 5), dpi = 300) # create the figure
    ax = fig.add_subplot(111)

    for spine_id in ['left', 'bottom']:
        ax.spines[spine_id].set_position('zero')
        ax.spines[spine_id].set_smart_bounds(True)
    for spine_id in ['right', 'top']:
        ax.spines[spine_id].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')                     

    func_to_call(ax = ax, **kwargs)    

    if add_grid:
        ax.grid(True, which='both')                # add a grid   

    if solution_object is not None:
        if solution_object['show_solutions']:
            label_friendly_solutions = []
            for solution in solution_object['solutions']:     
                label_friendly_solutions.append(solution[0] + " is " + str(solution[1]) + solution[2])
            plt.title('\n'.join(label_friendly_solutions)) 

    plt.tight_layout()          

    if save_file:
        # generate timestamp for the filename to make it unique
        now = str(datetime.now())
        for c in ['-', ' ', '.', ':']:
            now = now.replace(c, '_')
        # put together a filename and its path
        filename_with_path = os.path.expanduser('~/Documents/Python/Tutoring/Images/matlibplot' + now + '.png')
        plt.savefig(filename_with_path)    

    plt.show() # show! 

    if solution_object is not None:
        if not solution_object['show_solutions']:
            for solution in solution_object['solutions']:
                quiz_result = check_quiz_solution(what_are_we_looking_for = solution[0], 
                                                  correct_solution = solution[1], 
                                                  solution_units = solution[2])
                print('\n'.join(quiz_result))

    return filename_with_path

def plot_point(ax, x, y, colour = '', marker = '', annotiation = '', 
               show_coords = True, do_projections = True, do_lines = False,
               tolerance = 0.0001):
    if (abs(x) > tolerance) and (abs(y) > tolerance) and do_projections:
        if do_lines:
            ax.plot([x, x], [0, y], colour + ':', linewidth = 3)  
            ax.plot([0, x], [y, y], colour + ':', linewidth = 3)  
        plot_point(ax, x, 0, colour = colour, marker = marker, annotiation = annotiation + '_X')
        plot_point(ax, 0, y, colour = colour, marker = marker, annotiation = annotiation + '_Y')
    ax.plot([x], [y], colour + marker)
    annotation_label = annotiation 
    if show_coords:
        annotation_label += " (" + str(x) + ", " + str(y) + ")"
    ax.annotate(annotation_label, (x, y), fontsize = 8)

def plot_grid(ax, x, y):
    for _x, _y in [[x, y], [-x, y], [x, -y], [-x, -y]]:
        plot_point(ax, _x, _y, show_coords = False, do_projections = False)
    loc = mticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)
    ax.yaxis.set_major_locator(loc)

plt_envelope(plot_point, x = 1, y = 2, annotiation = 'A', colour = 'r', marker = 'o', do_lines = True)
plt_envelope(plot_grid, x = 10, y = 10, add_grid = True)


def create_vertical_arrow(arrow_x, 
                          arrowhead_width, # not used
                          arrowhead_tip_y, 
                          arrowhead_tip_height, 
                          end_shaft, 
                          colour_arrowhead = 'black',
                          colour_shaft = None): 
    if colour_shaft is None: # if we have not specified the colour of the shaft
        colour_shaft = colour_arrowhead # use the same colour as the colour of the arrowhead!

                                                            # define a symmetric 1-by-1 arrowhead
    arrowhead_outline = numpy.array([[-0.5, 1.0], [0.5, 1.0], [0.0, 0.0], [-0.5, 1.0]])   
    arrowhead_outline *= arrowhead_tip_height               # scale it
    if (end_shaft < arrowhead_tip_y):                       # if the end of the tip is above the end of the shaft,
        arrowhead_outline[:, 1] *= -1                       # flip it upside down
    arrowhead_outline[:, 0] += arrow_x                      # change X coords to move along OX axis
    arrowhead_outline[:, 1] += arrowhead_tip_y              # change Y coords to move along OY axis

    path = mpath.Path(arrowhead_outline)                    # create the outline of the arrowhead
    arrowhead = mpatches.PathPatch(path, 
                                   fc = colour_arrowhead, 
                                   ec = colour_arrowhead)   # fill in the outline

    # x = np.array([arrow_x, arrow_x])                      # define where the arrow line should go - X coordinates
    # y = np.array([arrowhead_tip_y, end_shaft])            # define where the arrow line should go - Y coordinates
    # ax.plot(x, y, color=colour_shaft)                     # add the arrow shaft to the figure

    shaft = mlines.Line2D([arrow_x, arrow_x], [arrowhead_tip_y, end_shaft], color=colour_shaft) # create the line - shaft
    
    return arrowhead, shaft