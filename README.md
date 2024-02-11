Threaded Portrait Generator
This project is a fun weekend endeavor aimed at creating threaded images by hand. It takes a black and white image and, based on a specified mesh length, plots points to create a meshed version of the image.
The end goal is to print the meshed image on an A4 paper, pin it on a board, and create a threaded image by hand.
It also available in web based form now at https://curious-turtle.github.io/ThreadedPortrait/

Installation:
git clone https://github.com/curious-turtle/ThreadedPortrait.git

Navigate to the project directory:
cd ThreadedPortrait

Install the required dependencies using pip:
pip install -r requirements.txt

Usage:
Once you have installed the dependencies, you can run the project by executing the following command:
python main.py

Step-by-Step Mode
You can enable step-by-step mode by using the -stepbystep flag. This mode displays the index of each point and prompts you to connect two points on each keypress of the Enter key in the terminal.
To run the project in step-by-step mode, use the following command:
python main.py -stepbystep

This will run the project and generate the meshed image based on the default settings. You can modify the mesh length and other parameters in the main.py file to customize the output.

Contributing
If you have any ideas for improvements or new features, feel free to contribute! Fork this repository, make your changes, and submit a pull request. Your contributions are always welcome.
License
This project is licensed under the MIT License.
Note: This project is created for educational and recreational purposes only. It is not intended for commercial use.
