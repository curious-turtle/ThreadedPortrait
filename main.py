from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from queue import Queue
import math

MESH_LENGTH=17
STEP=14
NEIGHBOURS=1
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
    direction=1
    for y in range(0,height,STEP):
      black_groups = getblackgroups(binary_image,y,width)
      #listofBlackcord.append(black_groups)
      temp_list=[]
      for ele in black_groups:
        temp_list.append((ele[0],-y))
        distance=ele[1]-ele[0]
        if distance>MESH_LENGTH:
          nodesToAdd=distance//MESH_LENGTH
          currentNode=ele[0]
          for _ in range(nodesToAdd):
            currentNode=currentNode+MESH_LENGTH
            temp_list.append((currentNode,-y))
        temp_list.append((ele[1],-y))
      if direction==1:
        direction=direction * -1
      else:
        direction=direction * -1
        temp_list.reverse()
      for node in temp_list:
        final_list.append(node)
    #print(final_list)
      

    #To test extreme cordinates form a boundary
    # for groups in listofBlackcord:
    #    if len(groups)>0:
    #       for group in groups:
    #         x_cord.append(group[0])
    #         y_cord.append(-group[1])

    # visited={}
    # neighbours={}
    lineGP=[]
    # for ele in final_list:
    #   visited[(ele[0],ele[1])]=False
    #   neighbours[(ele[0],ele[1])]=[]

    # my_queue=Queue()
    # my_queue.put(final_list[0])
    # while my_queue:
    #   ele=my_queue.get()
    #   visited[ele]=True
    #   currClosestNeb=findClosestElem(ele,final_list,neighbours)
    #   if(currClosestNeb==None):
    #     break
    #   neighbours[ele].append(currClosestNeb)
    #   neighbours[currClosestNeb].append(ele)
    #   my_queue.put(currClosestNeb)
    #   lineGP.append(ele)
    
    for ele in final_list:
      currClosestNeb=findClosestElemList(ele,final_list)
      #print(ele,"closest 4 neb",currClosestNeb)
      lineGP.append(ele)
      lineGP.append(currClosestNeb[0])
      # lineGP.append(ele)
      # lineGP.append(currClosestNeb[1])
      # lineGP.append(ele)
      # lineGP.append(currClosestNeb[2])
      # lineGP.append(ele)
      # lineGP.append(currClosestNeb[3])

    #To test scatter point plot
    for ele in lineGP:
       x_cord.append(ele[0])
       y_cord.append(ele[1])
    print(len(x_cord),len(y_cord))
    #plt.scatter(x_cord, y_cord,c="red",s=5)
    plt.plot(x_cord, y_cord,c="red",linewidth=1)
    plt.show()


#find closest such that it should not be current neighbour of ele
def findClosestElemList(src, final_list):
  min_distance = float('inf')
  closest_elem = None
  temp_dist_list=[]
  for candidate in final_list:
    #if not neighbours[ele] or candidate not in neighbours[ele]:
      if candidate!=src:
        distance = calculateDistance(src, candidate)
        temp_dist_list.append((distance,candidate))
  temp_dist_list.sort()
  list_to_return=[]
  for i in range(NEIGHBOURS):
    list_to_return.append(temp_dist_list[i][1])
  return list_to_return
      # if distance < min_distance:
      #   min_distance = distance
      #   closest_elem = candidate

  #return closest_elem

def calculateDistance(point1, point2):
  return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


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
#image_path = 'test.png'
create_binary_image(image_path)
    
    
    
#remove first element from front of queue and check all surrounding element
# if element is in x-1,y or x+1,y or x,y-1 or x,y+1 or x-1,y-1 or x-1,y+1 or x+1,y-1 or x+1,y+1 and is in set of listofBlackcord then remove it from set
# and if element is in set of listofBlackcord and is in range of 2 units (there will be 16 elements) then add it to my_queue

#Another idea is traverse each row in each row it will return list of tuples which are starting and ending index of black area
#and now check length between each of those black area and if it's more than define length then split it
#rinse and repeat