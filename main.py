from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from queue import Queue

def create_binary_image(image_path, threshold=128):
    image = Image.open(image_path)
    grayscale_image = image.convert('L')
    width, height = grayscale_image.size
    binary_image = np.zeros((height, width), dtype=np.uint8)
    print(height,width)
    for y in range(height):
      for x in range(width):
        if grayscale_image.getpixel((x, y)) > threshold:
          binary_image[y, x] = 255

    # Loop through each pixel in the grayscale image
    listofBlackcord=set()
    borderelements=set()
    my_queue=Queue()
    x_cord = []
    y_cord = []
    final_list=[]
    for y in range(height):
      for x in range(width):
        if binary_image[y, x] == 0:
          #x_cord.append(x)
          #y_cord.append(-y)
          listofBlackcord.add((x,y))
          if ((x-1>=0 and binary_image[y, x-1] == 255) or 
              (y-1 >=0 and binary_image[y-1, x] == 255) or 
              (x+1< width and binary_image[y, x+1] == 255) or 
              (y+1 <height and binary_image[y+1, x] == 255) or 
              (x==0 or x==width-1 or y==0 or y==height-1)):
            borderelements.add((x,y))
            my_queue.put((x,y))
            final_list.append((x,y))
    
    #remove first element from front of queue and check all surrounding element
    # if element is in x-1,y or x+1,y or x,y-1 or x,y+1 or x-1,y-1 or x-1,y+1 or x+1,y-1 or x+1,y+1 and is in set of listofBlackcord then remove it from set
    # and if element is in set of listofBlackcord and is in range of 2 units (there will be 16 elements) then add it to my_queue
    while not my_queue.empty():
      try:
          print(len(listofBlackcord))
          x, y = my_queue.get()
          inner_list,outer_list=findinoutlist(x,y)
          for inele in inner_list:
            if (inele in listofBlackcord and inele not in final_list):
              listofBlackcord.remove(inele)
          for outele in outer_list:
            if (outele in listofBlackcord and outele not in final_list):
              my_queue.put(outele)
              final_list.append((x,y))
      except MemoryError:
        continue  
    
    for ele in final_list:
       x_cord.append(ele[0])
       y_cord.append(-ele[1])
    print(len(x_cord),len(y_cord))
    plt.scatter(x_cord, y_cord,c="red")
    plt.show()

def findinoutlist(x,y,isize=2,osize=3):
    inner_list=[]
    for dx in range(-isize,isize+1):
      for dy in range(-isize,isize+1):
        inner_list.append((x+dx,y+dy))
    if (x,y) in inner_list:
      inner_list.remove((x,y))
    #print(inner_list)
    outer_list=[]
    for dx in range(-osize,osize+1):
     for dy in range(-osize,osize+1):
        outer_list.append((x+dx,y+dy))
    for innele in inner_list:
       if(innele in outer_list):
          outer_list.remove(innele)
    if (x,y) in inner_list:
      outer_list.remove((x,y))
    #print(outer_list)
    return inner_list,outer_list

# Example usage
image_path = 'mona_lisa_stencil_by_peoplperson_d1x04jb-pre.jpg'
create_binary_image(image_path)