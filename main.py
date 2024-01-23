from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

MESH_LENGTH=2
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
    listofBlackcord=[]
    x_cord = []
    y_cord = []
    final_list=[]
    # for y in range(height):
    #   for x in range(width):
    #     if binary_image[y, x] == 0:
    #       x_cord.append(x)
    #       y_cord.append(-y)

    for y in range(0,height,2):
      black_groups = getblackgroups(binary_image,y,width)
      listofBlackcord.append(black_groups)
      for ele in black_groups:
        distance=ele[1]-ele[0]
        if distance>MESH_LENGTH:
          nodesToAdd=distance//MESH_LENGTH
          currentNode=ele[0]
          for i in range(nodesToAdd):
            currentNode=currentNode+MESH_LENGTH
            final_list.append((currentNode,-y))
        final_list.append((ele[0],-y))
        final_list.append((ele[1],-y))

    # for groups in listofBlackcord:
    #    if len(groups)>0:
    #       for group in groups:
    #         x_cord.append(group[0])
    #         y_cord.append(-group[1])

    for ele in final_list:
       x_cord.append(ele[0])
       y_cord.append(ele[1])
    print(len(x_cord),len(y_cord))
    plt.scatter(x_cord, y_cord,c="red",s=0.1)
    plt.show()

def getblackgroups(binary_image,height,width):
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
image_path = 'mona_lisa_stencil_by_peoplperson_d1x04jb-pre.jpg'
create_binary_image(image_path)
    
    
    
#remove first element from front of queue and check all surrounding element
# if element is in x-1,y or x+1,y or x,y-1 or x,y+1 or x-1,y-1 or x-1,y+1 or x+1,y-1 or x+1,y+1 and is in set of listofBlackcord then remove it from set
# and if element is in set of listofBlackcord and is in range of 2 units (there will be 16 elements) then add it to my_queue

#Another idea is traverse each row in each row it will return list of tuples which are starting and ending index of black area
#and now check length between each of those black area and if it's more than define length then split it
#rinse and repeat