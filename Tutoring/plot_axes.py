import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
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

def axisEqual3D(ax):
    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)