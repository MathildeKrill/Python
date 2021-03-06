import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime
import os
import yu_quiz
import math

plt.rcParams.update({
    "font.size": 5,
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": [
         r"\usepackage[utf8x]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         r"\usepackage{cmbright}",
         ]
})

# this function returns the filename of the saved figure if we save it,
#            it returns None if we don't save it             
def plt_envelope(func_to_call, figsize, dpi, save_file = True, add_grid = False, 
                 tick_step = {'x' : 1.0, 'y' : 1.0},
                 solution_object = None, title_addon = None, tolerance = 0.0001,
                 **kwargs):
            
    fig = plt.figure(figsize = figsize, dpi = dpi) # create the figure
    ax = fig.add_subplot(111)

    func_to_call(ax = ax, **kwargs)    

    if add_grid: 
        # do spines      
        for spine_id in ['right', 'top']:
            ax.spines[spine_id].set_color('none')

        for spine_id, dim in [('bottom', 'x'), ('left', 'y')]:    
                
            low_bound, high_bound = getattr(ax, 'get_{}lim'.format(dim))()           
            if low_bound > 0:
                low_bound = 0
            if high_bound < 0:
                high_bound = 0
            first_tick = math.floor(low_bound / tick_step[dim]) * tick_step[dim]
            last_tick = math.ceil(high_bound / tick_step[dim]) * tick_step[dim]

            ax.spines[spine_id].set_position('zero')
            ax.spines[spine_id].set_bounds(first_tick, last_tick)
            ticks_this_axis = np.arange(first_tick, last_tick, tick_step[dim])
            getattr(ax, 'set_{}ticks'.format(dim))(ticks_this_axis)
            ax.spines[spine_id].set_bounds(first_tick, last_tick)

            # getattr(ax, '{}axis.set_ticks_position'.format(dim))(spine_id)
  
        ax.grid(True)


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
                quiz_result = yu_quiz.check_quiz_solution(what_are_we_looking_for = solution[0], 
                                                          correct_solution = solution[1], 
                                                          solution_units = solution_units,
                                                          tolerance = tolerance)
                print('\n'.join(quiz_result))

    return filename_with_path

from matplotlib import rc
from matplotlib import animation, rc
from IPython.display import HTML
rc('animation', html='jshtml')
plt.rcParams.update({
    "font.size": 10
})

def nice_axes(min_max_values_tick_freq, ax):
    # find max_extent (used for 3D only, but quick to find)
    max_extent = 0.
    for _min_max_values_tick_freq in min_max_values_tick_freq.values():
        extent = _min_max_values_tick_freq[1] - _min_max_values_tick_freq[0] 
        if max_extent < extent:
            max_extent = extent

    for dim, _min_max_values_tick_freq in min_max_values_tick_freq.items():

        # set the limits and make sure the aspects are equal
        min_this_axis = _min_max_values_tick_freq[0]
        max_this_axis = _min_max_values_tick_freq[1]
        if len(min_max_values_tick_freq) > 2:     
            # extend the limits for 3D because set_aspect("equal") is not implemented      
            min_this_axis = (min_this_axis + max_this_axis - max_extent) * 0.5
            max_this_axis = (min_this_axis + max_this_axis + max_extent) * 0.5
        else:
            ax.set_aspect("equal") 
        getattr(ax, 'set_{}lim'.format(dim))(min_this_axis, max_this_axis)

        # set ticks
        freq_this_axis=1.0
        if len(_min_max_values_tick_freq) > 2:
            freq_this_axis = _min_max_values_tick_freq[2]
        first_tick = math.floor(min_this_axis/freq_this_axis) * freq_this_axis
        last_tick = math.ceil(max_this_axis/freq_this_axis) * freq_this_axis
        ticks_this_axis = np.arange(first_tick, last_tick, freq_this_axis)
        getattr(ax, 'set_{}ticks'.format(dim))(ticks_this_axis)

def run_animation(func_name, fargs, projection='rectilinear', figsize=(7, 7), nb_frames=10, interval=500):   
    fig = plt.figure(figsize=figsize)
    ax = fig.gca(projection=projection)
    nb_frames = nb_frames
    anim = animation.FuncAnimation(fig, func_name, fargs=[ax, nb_frames] + fargs,
                               frames=nb_frames, interval=interval)
    return anim