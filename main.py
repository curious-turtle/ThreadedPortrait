from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-stepbystep', action='store_true', help='Run the animation step by step')
args = parser.parse_args()
step_by_step = args.stepbystep

def Run(image_path,mesh_length=10,threshold=128):
    STEP = mesh_length
    MESH_LENGTH = mesh_length
    
    image = Image.open(image_path)
    grayscale_image = image.convert('L')
    width, height = grayscale_image.size
    binary_image = np.zeros((height, width), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            if grayscale_image.getpixel((x, y)) > threshold:
                binary_image[y, x] = 255

    list_of_black_cord = []

    for y in range(0, height, STEP):
        black_groups = getblackgroups(binary_image, y, width)
        temp_list = []

        for ele in black_groups:
            temp_list.append((ele[0], -y))
            distance = ele[1] - ele[0]
            if distance > MESH_LENGTH:
                nodes_to_add = distance // MESH_LENGTH
                current_node = ele[0]
                for _ in range(nodes_to_add):
                    current_node = current_node + MESH_LENGTH
                    temp_list.append((current_node, -y))
                temp_list.append((ele[1], -y))

        for node in temp_list:
            list_of_black_cord.append(node)

    visited = {}
    tracker={}
    index=1
    for ele in list_of_black_cord:
        visited[ele] = False
        tracker[ele]=index
        index+=1

    fig, ax = plt.subplots()
    
    # Show scatter points at the beginning
    x_cord = [ele[0] for ele in list_of_black_cord]
    y_cord = [ele[1] for ele in list_of_black_cord]
    scatter = ax.scatter(x_cord, y_cord, c="blue", s=1)
    
    if step_by_step:
        for ele in list_of_black_cord:
            ax.text(ele[0], ele[1], str(tracker[ele]), fontsize=8, color='blue')

        ax.set_xlim(0, width)
        ax.set_ylim(-height, 0)
        
        print("Press Enter to after every connection to continue")
    
    def update(frame):
        nonlocal visited

        ele = list(visited.keys())[frame]
        visited[ele] = True
        curr_closest_neb_list = find_closest_elem_list(ele, list_of_black_cord)

        for curr_closest_neb in curr_closest_neb_list:
            if step_by_step:
                print(f"Connect {tracker[ele]} --> {tracker[curr_closest_neb]}")
                input("")
            line = ax.plot([ele[0], curr_closest_neb[0]], [ele[1], curr_closest_neb[1]], c="red", linewidth=1)[0]
    anim = FuncAnimation(fig, update, frames=len(visited), repeat=False,interval=2)
    plt.show()

def find_closest_elem_list(src, final_list):
    NEIGHBORS = 4
    temp_dist_list = []

    for candidate in final_list:
        if candidate != src:
            distance = calculate_distance(src, candidate)
            temp_dist_list.append((distance, candidate))

    temp_dist_list.sort()
    list_to_return = []

    for i in range(NEIGHBORS):
        list_to_return.append(temp_dist_list[i][1])

    return list_to_return

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def getblackgroups(binary_image, height, width):
    groups = []
    start = None

    for x in range(width):
        if binary_image[height, x] == 0 and start is None:
            start = x
        elif binary_image[height, x] != 0 and start is not None:
            groups.append((start, x))
            start = None

    if start is not None:
        groups.append((start, width - 1))

    return groups

# Example usage
image_path = 'flashImage.png'
Run(image_path)
