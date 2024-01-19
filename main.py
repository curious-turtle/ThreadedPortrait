from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def create_binary_image(image_path, threshold=128):
    image = Image.open(image_path)
    grayscale_image = image.convert('L')
    width, height = grayscale_image.size
    binary_image = np.zeros((height, width), dtype=np.uint8)
    
    for y in range(height):
      for x in range(width):
        if grayscale_image.getpixel((x, y)) > threshold:
          binary_image[y, x] = 255
    x_cord = []
    y_cord = []

    # # Loop through each pixel in the grayscale image
    for y in range(height):
        for x in range(width):
            if binary_image[y, x] == 0:
              x_cord.append(x)
              y_cord.append(-y)
    print(len(x_cord))
    #plt.scatter(x_cord, y_cord, s=0.01)
    #plt.show()

# Example usage
image_path = 'mona_lisa_stencil_by_peoplperson_d1x04jb-pre.jpg'
create_binary_image(image_path)