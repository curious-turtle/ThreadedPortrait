// Log:
// AK97 24-02-10: Creation convert image to greyscale and get binary image out of it

function Run(imagePath, meshLength = 10, threshold = 128) {
  const STEP = meshLength;
  const MESH_LENGTH = meshLength;

  const img = new Image();
  img.onload = function () {
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');

    // Set the size of the temporary canvas
    tempCanvas.width = img.width;
    tempCanvas.height = img.height;

    // Draw the image on the temporary canvas
    tempCtx.drawImage(img, 0, 0);

    const imageData = tempCtx.getImageData(0, 0, tempCanvas.width, tempCanvas.height);
    const grayscaleData = toGrayscale(imageData, tempCtx);
    const binaryData = toBinary(grayscaleData, threshold, tempCtx);

    const animationCanvas = document.getElementById('animationCanvas');
    const animationCtx = animationCanvas.getContext('2d');

    animationCanvas.width = binaryData.width;
    animationCanvas.height = binaryData.height;
    console.log(animationCanvas.width, animationCanvas.height);

    // Draw the scaled image onto the animationCanvas
    animationCtx.putImageData(binaryData, 0, 0);

  };
  img.onerror = function () {
    console.error("Error loading image:", imagePath);
  };
  img.src = imagePath.name;
}

function toGrayscale(imageData, ctx) {
  const grayscaleData = ctx.createImageData(imageData.width, imageData.height);
  console.log("Length of grayscaleData:", grayscaleData);
  for (let i = 0; i < imageData.data.length; i += 4) {
    const avg = (imageData.data[i] + imageData.data[i + 1] + imageData.data[i + 2]) / 3;
    grayscaleData.data[i] = avg; // Red
    grayscaleData.data[i + 1] = avg; // Green
    grayscaleData.data[i + 2] = avg; // Blue
    grayscaleData.data[i + 3] = imageData.data[i + 3]; // Alpha
  }
  return grayscaleData;
}

function toBinary(grayscaleData, threshold, ctx) {

  const binaryData = ctx.createImageData(grayscaleData.width, grayscaleData.height);

  for (let i = 0; i < grayscaleData.data.length; i += 4) {
    const intensity = grayscaleData.data[i];
    const value = intensity > threshold ? 255 : 0;
    binaryData.data[i] = value; // Red
    binaryData.data[i + 1] = value; // Green
    binaryData.data[i + 2] = value; // Blue
    binaryData.data[i + 3] = grayscaleData.data[i + 3]; // Alpha
  }
  return binaryData;
}



function getBlackGroups(binaryData, height) {
  const groups = [];
  let start = null;
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      if (binaryData[y * width + x] === 0 && start === null) {
        start = x;
      } else if (binaryData[y * width + x] !== 0 && start !== null) {
        groups.push([start, x]);
        start = null;
      }
    }
    if (start !== null) {
      groups.push([start, width - 1]);
      start = null;
    }
  }
  return groups;
}

function findClosestElemList(src, finalList) {
  const NEIGHBORS = 4;
  const tempDistList = [];
  for (const candidate of finalList) {
    if (candidate[0] !== src[0] || candidate[1] !== src[1]) {
      const distance = calculateDistance(src, candidate);
      tempDistList.push([distance, candidate]);
    }
  }
  tempDistList.sort((a, b) => a[0] - b[0]);
  const listToReturn = [];
  for (let i = 0; i < NEIGHBORS; i++) {
    listToReturn.push(tempDistList[i][1]);
  }
  return listToReturn;
}

function calculateDistance(point1, point2) {
  return Math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2);
}
