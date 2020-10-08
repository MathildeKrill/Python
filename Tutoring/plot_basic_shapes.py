import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker as mticker

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
    X, Y, Z = cuboid_data( pos, size )
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, **kwargs)


def create_polygon(ax, all_x, all_y, style = '-', annotate = False, add_rectangle_around = False, 
                   fill_in_colour = None, outline_style='c:', linewidth = 3):
    
    point_labels = [chr(i) for i in range (65, 91)]          # ['A', 'B', 'C', ... 'Z']
    ax.set_aspect("equal")  

    if add_rectangle_around:
        min_x = min(all_x)
        max_x = max(all_x)
        min_y = min(all_y)
        max_y = max(all_y)
        create_polygon(all_x=[min_x, max_x, max_x, min_x, min_x], # recursive call
                       all_y=[min_y, min_y, max_y, max_y, min_y],
                       ax=ax, 
                       style=outline_style)

    for i in range(len(all_x) - 1):                          # plot the sides of our polygon
        x_bar = np.array([all_x[i], all_x[i+1]])
        y_bar = np.array([all_y[i], all_y[i+1]]) 
        ax.plot(x_bar, y_bar, style, color = fill_in_colour, linewidth = linewidth)          # plot
        if annotate:                                         # annotate
            plot_point(ax, all_x[i], all_y[i], annotiation = point_labels[i % 26])

    if fill_in_colour is not None:
        outline = [[x, y] for x, y in list(zip(all_x, all_y))]
        fill_in_outline(ax, outline, fill_in_colour)


def create_polygons(ax, params_polygons, params_points = [], colour_point = 'k', marker = 'o', show_coords = True):
    for params_polygon in params_polygons:
        create_polygon(ax, **params_polygon)
    for params_point in params_points:
        params_point['colour'] = colour_point
        params_point['marker'] = marker
        params_point['show_coords'] = show_coords
        plot_point(ax, **params_point)
