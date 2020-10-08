import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker as mticker
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
import os

plt.rcParams.update({
    "font.size": 5,
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": [
         r"\usepackage[utf8x]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         r"\usepackage{cmbright}",
         ]
})

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

# this function returns the filename of the saved figure if we save it,
#            it returns None if we don't save it             
def plt_envelope(func_to_call, figsize, dpi, save_file = True, add_grid = False, 
                 x_tick_step = 1.0, y_tick_step = 1.0,
                 solution_object = None, title_addon = None, tolerance = 0.0001,
                 **kwargs):
            
    fig = plt.figure(figsize = figsize, dpi = dpi) # create the figure
    ax = fig.add_subplot(111)

    func_to_call(ax = ax, **kwargs)    

    if add_grid: 
        # do spines
        for spine_id in ['left', 'bottom']:
            ax.spines[spine_id].set_position('zero')
            ax.spines[spine_id].set_smart_bounds(True)
        for spine_id in ['right', 'top']:
            ax.spines[spine_id].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')                     

        # make sure 0s are included in 0X
        left_x, right_x = ax.get_xlim()  # return the current xlim
        if left_x > 0:
            left_x -= np.ceil(left_x)
            ax.set_xlim(left = left_x)
        if right_x < 0:
            right_x -= np.floor(left_x)
            ax.set_xlim(right = right_x)
        ax.spines['bottom'].set_bounds(left_x, right_x)
        #ax.set_xlim(left_x, right_x)
        loc_x = mticker.MultipleLocator(base=x_tick_step) # this locator puts ticks at regular intervals
        ax.xaxis.set_major_locator(loc_x)
        loc_x.set_bounds(vmin = left_x, vmax = right_x)
        
        # make sure 1s are included in 0Y
        bottom_y, top_y = ax.get_ylim()  # return the current ylim
        if bottom_y > 0:
            bottom_y -= np.ceil(bottom_y)
            ax.set_ylim(bottom = bottom_y)
        if top_y < 0:
            top_y -= np.floor(top_y)
            ax.set_ylim(top = top_y)
        ax.spines['left'].set_bounds(bottom_y, top_y)
        #ax.set_ylim(bottom_y, top_y)
        loc_y = mticker.MultipleLocator(base=y_tick_step) # this locator puts ticks at regular intervals
        ax.yaxis.set_major_locator(loc_y)
        loc_y.set_bounds(vmin = bottom_y, vmax = top_y)

        #xtick_locs, _ = plt.xticks()  
        ax.grid(add_grid, which='both')#, xdata=xtick_locs, ydata=ax.get_yticks())  # add a grid 


    if solution_object is not None:
        if solution_object['show_solutions']:
            label_friendly_solutions = []
            for solution in solution_object['solutions']: 
                solution_sentence = solution[0] + " is " + str(solution[1])
                if len(solution) > 2:
                    solution_sentence += solution[2]
                label_friendly_solutions.append(solution_sentence)
            label_friendly_solutions.append("")
            plt.title('\n'.join(label_friendly_solutions)) 

    if title_addon is not None:
        plt.suptitle(title_addon)

    plt.tight_layout()         

    if save_file:
        # generate timestamp for the filename to make it unique
        now = str(datetime.now())
        for c in ['-', ' ', '.', ':']:
            now = now.replace(c, '_')
        # put together a filename and its path
        filename_with_path = os.path.expanduser('~/Documents/PythonImages/matlibplot' + now + '.jpg')
        plt.savefig(filename_with_path)  
    else:
        filename_with_path = None  

    plt.show() # show! 

    if solution_object is not None:
        if not solution_object['show_solutions']:
            for solution in solution_object['solutions']:
                if len(solution) > 2:
                    solution_units = solution[2]
                else:
                    solution_units = None
                quiz_result = check_quiz_solution(what_are_we_looking_for = solution[0], 
                                                  correct_solution = solution[1], 
                                                  solution_units = solution_units,
                                                  tolerance = tolerance)
                print('\n'.join(quiz_result))

    return filename_with_path

def plot_point(ax, x, y, colour = '', marker = '', annotiation = '', 
               show_coords = True, do_projections = False, do_lines = False,
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
    ax.annotate(annotation_label, (x, y))

def plot_grid(ax, x, y):
    for _x, _y in [[x, y], [-x, y], [x, -y], [-x, -y]]:
        plot_point(ax, _x, _y, show_coords = False, do_projections = False)
    loc = mticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)
    ax.yaxis.set_major_locator(loc)

#plt_envelope(plot_grid, x = 10, y = 10, add_grid = True)

def fill_in_outline(ax, outline, fill_in_colour):
    path = mpath.Path(outline)                    # create the outline of the arrowhead
    patch = mpatches.PathPatch(path, 
                               fc = fill_in_colour, 
                               ec = fill_in_colour)   # fill in the outline
    ax.add_patch(patch)

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
    arrowhead_outline = np.array([[-0.5, 1.0], [0.5, 1.0], [0.0, 0.0], [-0.5, 1.0]])   
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

def draw_ruler(ax, min_x, nb_steps, size_step, big_bar_frequency, y_lim_small, y_lim_big):
    ax.plot([min_x, min_x + nb_steps * size_step], [0, 0])              # add a horizontal line to the plot

    for i in range(nb_steps + 1):                # create (nb_steps + 1) vertical bars,
        x = min_x + i * size_step                # define where we put this vertical bar
        x_bar = np.array([x, x])                 # define the vertical bar - X coords

        y_lim = y_lim_small                      # this is the default size of the vertical bar
        if (i % big_bar_frequency == 0):         # these bars will be longer
            y_lim = y_lim_big     
        y_bar = np.array([-y_lim, y_lim])        # define the vertical bar - Y coords

        ax.plot(x_bar, y_bar)

def draw_square(ax, min_x, min_y, length, fill_in_colour):

    ax.set_aspect("equal")  

    all_x = [min_x, min_x + length, min_x + length, min_x, min_x]
    all_y = [min_y, min_y, min_y + length, min_y + length, min_y]
    
    for i in range(4):                          # plot the sides of our polygon
        x_bar = np.array([all_x[i], all_x[i+1]])
        y_bar = np.array([all_y[i], all_y[i+1]]) 
        ax.plot(x_bar, y_bar, color = fill_in_colour, linewidth = 1)

    if fill_in_colour is not None:
        outline = [[x, y] for x, y in list(zip(all_x, all_y))]
        fill_in_outline(ax, outline, fill_in_colour)

def draw_squares(ax, min_x, min_y, nb_x, nb_y, length, fill_in_colour, gap = 0, skip_x = []):
    for i_x in range(nb_x):
        if i_x in skip_x:
            continue
        _min_x = min_x + i_x * (length + gap)
        for i_y in range(nb_y):
            _min_y = min_y + i_y * (length + gap)
            draw_square(ax, min_x = _min_x, min_y = _min_y, length = length, fill_in_colour = fill_in_colour)

def cuboid_data(o, size=(1,1,1)):
    # code taken from
    # https://stackoverflow.com/a/35978146/4124317
    # suppose axis direction: x: to left; y: to inside; z: to upper
    # get the length, width, and height
    l, w, h = size
    x = [[o[0], o[0] + l, o[0] + l, o[0], o[0]],  
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],  
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],  
         [o[0], o[0] + l, o[0] + l, o[0], o[0]]]  
    y = [[o[1], o[1], o[1] + w, o[1] + w, o[1]],  
         [o[1], o[1], o[1] + w, o[1] + w, o[1]],  
         [o[1], o[1], o[1], o[1], o[1]],          
         [o[1] + w, o[1] + w, o[1] + w, o[1] + w, o[1] + w]]   
    z = [[o[2], o[2], o[2], o[2], o[2]],                       
         [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],   
         [o[2], o[2], o[2] + h, o[2] + h, o[2]],               
         [o[2], o[2], o[2] + h, o[2] + h, o[2]]]               
    return np.array(x), np.array(y), np.array(z)

def plotCubeAt(pos=(0,0,0), size=(1,1,1), ax=None,**kwargs):
    # Plotting a cube element at position pos
    if ax !=None:
        X, Y, Z = cuboid_data( pos, size )
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, **kwargs)

def axisEqual3D(ax):
    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)