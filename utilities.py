import numpy as np
import matplotlib.pyplot as plt
import pickle

angle_names = ["E", "ENE", "NE", "NNE", "N", "NNW", "NW", "WNW", "W", "WSW", "SW", "SSW", "S", "SSE", "SE", "ESE"] 

def load_object(file_name): 
    with open(file_name, 'rb') as file_object:
        data = pickle.load(file_object) 
        file_object.close()
        return data
    
def save_object(file_name, std1):       
    with open(file_name, 'wb') as file_object:
        pickle.dump(std1, file_object) 
        file_object.close()

def random_colors(num_colors):
    colors_set = []
    for x in range(num_colors):
        string_color = "#"
        while string_color == "#" or string_color in colors_set:
            string_color = "#"
            set_letters = "0123456789ABCDEF"
            for y in range(6):
                string_color += set_letters[np.random.randint(0, 16)]
        colors_set.append(string_color)
    return colors_set

def make_circles(radius_steps, angle_offsets, scaling_factor = 1, xoffset = 0, yoffset = 0, angle_depth = 3):
 
    for ra in radius_steps:
        x_coords_circle = [xoffset + scaling_factor * ra * np.cos(angle / 180 * np.pi) for angle in np.arange(0.0001, 360)]
        y_coords_circle = [yoffset + scaling_factor * ra * np.sin(angle / 180 * np.pi) for angle in np.arange(0.0001, 360)]
        plt.plot(x_coords_circle, y_coords_circle, c = "k", zorder = 1)

    for angle in angle_offsets:
        x_coords_line = [xoffset + scaling_factor * ra * np.cos(angle / 180 * np.pi) for ra in np.arange(radius_steps[0], radius_steps[-1] + 0.01, 0.01)]
        y_coords_line = [yoffset + scaling_factor * ra * np.sin(angle / 180 * np.pi) for ra in np.arange(radius_steps[0], radius_steps[-1] + 0.01, 0.01)]
        plt.plot(x_coords_line, y_coords_line, c = "k", zorder = 1)

    if angle_depth > 0:
        
        names_of_angles = []

        for an in angle_names:
            if len(an) > angle_depth:
                continue
            names_of_angles.append(an)

        amount_of_angle = np.arange(0, 360, 360 / len(names_of_angles))

        tmp_ra = radius_steps[-1] + (radius_steps[-1] - radius_steps[-2]) * 1.5
        tmp_ra_larger = (radius_steps[-1] + (radius_steps[-1] - radius_steps[-2])) * 3

        x_coords_circle = [xoffset + scaling_factor * tmp_ra_larger * np.cos(angle / 180 * np.pi) for angle in np.arange(0.0001, 360)]
        y_coords_circle = [yoffset + scaling_factor * tmp_ra_larger * np.sin(angle / 180 * np.pi) for angle in np.arange(0.0001, 360)]
        plt.plot(x_coords_circle, y_coords_circle, c = "white", zorder = 1)

        for ix, angle in enumerate(amount_of_angle):

            x_coords_marker = xoffset + scaling_factor * tmp_ra * np.cos(angle / 180 * np.pi) - len(names_of_angles[ix]) / 4 * (radius_steps[-1] - radius_steps[-2])
            y_coords_marker = yoffset + scaling_factor * tmp_ra * np.sin(angle / 180 * np.pi) - 1 / 4 * (radius_steps[-1] - radius_steps[-2])

            plt.text(x_coords_marker, y_coords_marker, names_of_angles[ix])
 
def plot_arc(lnm, radius, start_radius, start, end, color_use = "blue", draw_edges = True, scaling_factor = 1, xoffset = 0, yoffset = 0, use_label = False):
   
    if radius == 0:
        return
     
    if start > end:
        start = start - 360

    old_start = start
    old_end = end

    for v in range(4): 
        if end >= v * 90 and end < (v + 1) * 90:
            q = v + 1
        
    xsgn = 1
    ysgn = 1

    if q == 2:

        start = 180 - start
        end = 180 - end
        xsgn = -1

    if q == 3:

        start = start - 180
        end = end - 180
        xsgn = -1 
        ysgn = -1
        
    if q == 4:

        start = 360 - start 
        end = 360 - end
        ysgn = -1

    start, end = min(end, start), max(end, start)

    x_coords_arc = [xoffset + scaling_factor * xsgn * radius * np.cos(angle / 180 * np.pi) for angle in np.arange(start, end + 0.01, 0.01)]
    y_coords_arc = [yoffset + scaling_factor * ysgn * radius * np.sin(angle / 180 * np.pi) for angle in np.arange(start, end + 0.01, 0.01)]
    if draw_edges:
        plt.plot(x_coords_arc, y_coords_arc, c = "k", zorder = 3)

    x_coords_arcb = [xoffset + scaling_factor * xsgn * start_radius * np.cos(angle / 180 * np.pi) for angle in np.arange(start, end + 0.01, 0.01)]
    y_coords_arcb = [yoffset + scaling_factor * ysgn * start_radius * np.sin(angle / 180 * np.pi) for angle in np.arange(start, end + 0.01, 0.01)]
    if draw_edges:  
        plt.plot(x_coords_arcb, y_coords_arcb, c = "k", zorder = 3)

    x_coords_s = [xoffset + scaling_factor * xsgn * ra * np.cos(start / 180 * np.pi) for ra in np.arange(start_radius, radius + 0.01, 0.01)]
    y_coords_s = [yoffset + scaling_factor * ysgn * ra * np.sin(start / 180 * np.pi) for ra in np.arange(start_radius, radius + 0.01, 0.01)]
    if draw_edges:  
        plt.plot(x_coords_s, y_coords_s, c = "k", zorder = 3)

    x_coords_e = [xoffset + scaling_factor * xsgn * ra * np.cos(end / 180 * np.pi) for ra in np.arange(start_radius, radius + 0.01, 0.01)]
    y_coords_e = [yoffset + scaling_factor * ysgn * ra * np.sin(end / 180 * np.pi) for ra in np.arange(start_radius, radius + 0.01, 0.01)]
    if draw_edges:  
        plt.plot(x_coords_e, y_coords_e, c = "k", zorder = 3) 

    x_start_new = max(abs(x_coords_s[0] - xoffset) / scaling_factor, abs(x_coords_arc[-1] - xoffset) / scaling_factor)
    
    start_radius_new = x_start_new / np.cos(start / 180 * np.pi)   
    x_coords_s_1 = [xoffset + scaling_factor * xsgn * ra * np.cos(start / 180 * np.pi) for ra in np.arange(start_radius_new, radius + 0.01, 0.01)]
    y_coords_s_1 = [yoffset + scaling_factor * ysgn * ra * np.sin(start / 180 * np.pi) for ra in np.arange(start_radius_new, radius + 0.01, 0.01)] 

    x_coords_arc_1 = x_coords_s_1
    y_coords_arc_1 = [yoffset + scaling_factor * ysgn * radius * np.sin(np.arccos(abs(xval - xoffset) / scaling_factor / radius)) for xval in x_coords_arc_1] 

    if end < 90 and start > 0:
        if use_label:
            plt.fill_between(x_coords_s_1, y_coords_arc_1, y_coords_s_1, color = color_use, zorder = 2, label = lnm) 
            use_label = False
        else:
            plt.fill_between(x_coords_s_1, y_coords_arc_1, y_coords_s_1, color = color_use, zorder = 2)

    x_end_new = min(abs(x_coords_e[-1] - xoffset) / scaling_factor, abs(x_coords_arcb[0] - xoffset) / scaling_factor)    

    end_radius_new = x_end_new / np.cos(end / 180 * np.pi)  
    x_coords_e_1 = [xoffset + scaling_factor * xsgn * ra * np.cos(end / 180 * np.pi) for ra in np.arange(start_radius, end_radius_new + 0.01, 0.01)]
    y_coords_e_1 = [yoffset + scaling_factor * ysgn * ra * np.sin(end / 180 * np.pi) for ra in np.arange(start_radius, end_radius_new + 0.01, 0.01)]

    x_coords_arcb_1 = x_coords_e_1
    y_coords_arcb_1 = [yoffset + scaling_factor * ysgn * start_radius * np.sin(np.arccos(abs(xval - xoffset) / scaling_factor / start_radius)) for xval in x_coords_arcb_1]  

    if end < 90 and start > 0:
        if use_label:
            plt.fill_between(x_coords_e_1, y_coords_e_1, y_coords_arcb_1, color = color_use, zorder = 2, label = lnm)
            use_label = False
        else:
            plt.fill_between(x_coords_e_1, y_coords_e_1, y_coords_arcb_1, color = color_use, zorder = 2)

    x_coords_rest = np.arange(x_end_new, x_start_new + 0.01, 0.01)
    x_coords_rest = [xoffset + scaling_factor * xsgn * val for val in x_coords_rest]

    if abs(x_coords_s[0] - xoffset) / scaling_factor < abs(x_coords_arc[-1] - xoffset) / scaling_factor and end < 90 and start > 0:
        y_coords_s_2 = [yoffset + scaling_factor * ysgn * abs(xval - xoffset) / scaling_factor / np.cos(start / 180 * np.pi) * np.sin(start / 180 * np.pi) for xval in x_coords_rest] 
        y_coords_e_2 = [yoffset + scaling_factor * ysgn * abs(xval - xoffset) / scaling_factor / np.cos(end / 180 * np.pi) * np.sin(end / 180 * np.pi) for xval in x_coords_rest]     
        
        if use_label:
            plt.fill_between(x_coords_rest, y_coords_e_2, y_coords_s_2, color = color_use, zorder = 2, label = lnm)
            use_label = False
        else:
            plt.fill_between(x_coords_rest, y_coords_e_2, y_coords_s_2, color = color_use, zorder = 2) 
        
    if abs(x_coords_s[0] - xoffset) / scaling_factor > abs(x_coords_arc[-1] - xoffset) / scaling_factor:
        y_coords_arc_2 = [yoffset + scaling_factor * ysgn * radius * np.sin(np.arccos(abs(xval - xoffset) / scaling_factor / radius)) for xval in x_coords_rest] 
        y_coords_arcb_2 = [yoffset + scaling_factor * ysgn * start_radius * np.sin(np.arccos(abs(xval - xoffset) / scaling_factor / start_radius)) for xval in x_coords_rest]
        
        if use_label:
            plt.fill_between(x_coords_rest, y_coords_arc_2, y_coords_arcb_2, color = color_use, zorder = 2, label = lnm)
            use_label = False
        else:
            plt.fill_between(x_coords_rest, y_coords_arc_2, y_coords_arcb_2, color = color_use, zorder = 2)

    if end > 90 or start < 0:

        for v in range(0, 360, 90):
            if v >= old_start and v <= old_end:
                midv = v
                break

        plot_arc(lnm, radius, start_radius, (360 + old_start) % 360, (360 + midv - 0.0001) % 360, color_use = color_use, draw_edges = False, scaling_factor = scaling_factor, xoffset = xoffset, yoffset = yoffset, use_label = use_label)
        plot_arc(lnm, radius, start_radius, midv + 0.0001, old_end, color_use = color_use, draw_edges = False, scaling_factor = scaling_factor, xoffset = xoffset, yoffset = yoffset, use_label = False)
  