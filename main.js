// Log:
// AK97 24-02-10: Creation convert image to greyscale and get binary image out of it
// AK97 24-02-10: Added plotPoints to plot points based on mesh_length
// AK97 24-02-10: Added animation there is one minor bug it starts from top left corner for some reason. Will fix later

function Run(imagePath, meshLength = 10, threshold = 128) {
  const STEP = meshLength;
  const MESH_LENGTH = meshLength;

  const img = new Image();
  img.onload = async function () {
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');

    // Set the size of the temporary canvas
    width = img.width;
    height = img.height;

    tempCanvas.width = width;
    tempCanvas.height = height;

    // Draw the image on the temporary canvas
    tempCtx.drawImage(img, 0, 0);
    const imageData = tempCtx.getImageData(0, 0, tempCanvas.width, tempCanvas.height);
    const grayscaleData = toGrayscale(imageData, threshold);

    const animationCanvas = document.getElementById('animationCanvas');
    animationCanvas.width = grayscaleData[0].length * 1; // Adjust width as needed
    animationCanvas.height = grayscaleData.length * 1;

    let listofBlackcord = [];
    for (let y = 0; y < img.height; y += STEP) {
      let black_groups = getBlackGroups(grayscaleData, y, width);
      let temp_list = [];

      for (ele of black_groups) {
        temp_list.push([ele[0], -y]);
        let distance = ele[1] - ele[0];
        if (distance > MESH_LENGTH) {
          const nodes_to_add = Math.floor(distance / MESH_LENGTH);
          let current_node = ele[0];
          for (let i = 0; i < nodes_to_add; i++) {
            current_node += MESH_LENGTH;
            temp_list.push([current_node, -y]);
          }
          temp_list.push([ele[1], -y]);
        }
      }
      for (node of temp_list)
        listofBlackcord.push(node)
    }
    plotPoints(listofBlackcord, animationCanvas);

    let visited = new Map();
    let lineGP = [];

    listofBlackcord.forEach((arr) => {
      visited.set(arr, false);
    });
    let myStack = [];
    while (true) {
      let notVisitedCount = 0;
      for (let [key, value] of visited.entries()) {
        if (value == false) {
          myStack.push(key);
          notVisitedCount++;
          break
        }
      }
    if (notVisitedCount === 0) {
      break;
    }
    while (myStack.length > 0) {
      let ele = myStack.pop();
      if (!visited.get(ele)) {
        visited.set(ele, true);;
        let currClosestNebList = findClosestElemList(ele, listofBlackcord);
        for (let currClosestNeb in currClosestNebList) {
          myStack.push(currClosestNebList[currClosestNeb]);
          lineGP.push(currClosestNebList[currClosestNeb]);
          lineGP.push(currClosestNebList[currClosestNeb]);
        }
      } else {
        lineGP.push(ele);
      }
    }
  }
  console.log(lineGP)
  animateLines(lineGP, animationCanvas);

};
img.onerror = function () {
  console.error("Error loading image:", imagePath);
};
img.src = imagePath;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function toGrayscale(imageData, threshold) {
  //const grayscaleData = ctx.createImageData(imageData.width, imageData.height);
  let grayscaleData = [];
  for (let y = 0; y < imageData.height; y++) {
    grayscaleData.push([]);
    for (let x = 0; x < imageData.width; x++) {
      grayscaleData[y].push(0); // Initialize each element to 0
    }
  }

  let i = 0;
  for (let y = 0; y < imageData.height; y++) {
    for (let x = 0; x < imageData.width; x++) {
      const avg = (imageData.data[i] + imageData.data[i + 1] + imageData.data[i + 2]) / 3;
      const value = avg > threshold ? 255 : 0;
      grayscaleData[y][x] = value;
      i += 4;
    }
  }
  return grayscaleData;
}

function getBlackGroups(grayscaleData, height, width) {
  let groups = [];
  let start = null;

  for (let x = 0; x < width; x++) {
    if (grayscaleData[height][x] === 0 && start === null) {
      start = x;
    } else if (grayscaleData[height][x] !== 0 && start !== null) {
      groups.push([start, x]);
      start = null;
    }
  }
  if (start !== null) {
    groups.push([start, width - 1]);
    start = null;
  }
  return groups;
}

function plotPoints(grayscaleData, canvas) {
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = 'black';
  grayscaleData.forEach(coord => {
    const [x, y] = coord;
    ctx.fillRect(x, -y, 1, 1);
  });
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

function animateLines(lineGP, canvas) {
  let ctx = canvas.getContext('2d');
  let frame = 0;
  let lastFrameTime = 0; // Keep track of the last frame time

  function drawFrame(currentTime) {
    if (frame >= lineGP.length) {
      return;
    }

    // Calculate the time elapsed since the last frame
    let deltaTime = currentTime - lastFrameTime;

    // Only draw a frame if enough time has passed
    if (deltaTime > 1) { // Adjust the delay here (e.g., 100 milliseconds)
      let ele = lineGP[frame];
      let next = lineGP[frame + 1];

      ctx.beginPath();
      ctx.moveTo(ele[0], -ele[1]);
      ctx.lineTo(next[0], -next[1]);
      ctx.strokeStyle = 'red'; // Set line color
      ctx.lineWidth = 1; // Set line width
      ctx.stroke();

      frame++;
      lastFrameTime = currentTime;
    }

    requestAnimationFrame(drawFrame);
  }

  requestAnimationFrame(drawFrame);
}
