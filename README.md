# Calendar Shifting
## Overview
The project is to take in any .ics file and a date that the user wishes to shift the first event to and return a modified .ics file with the shifted events and the same calendar details.
## Architecture
The application is implemented using python's flask framework. The application is also written with python and utilizes the icalendar and datetime packages
## High Level Flow Diagram
![c3809cfdf9b0aed0decc81f25f7afa30.png](:/fa2bb449efa244999da0cca7a83c4ca4)
## Usage
1. Make sure python 3.5+ is installed on your machine
2. Clone the github repository located at 
3. Navigate to the directory in terminal
4. Run the controller.py file using python3 controller.py and open the url that shows up in terminal 


![Screen Shot 2020-06-14 at 11.17.42 PM.png](:/f7f4c45a41e74ce4ba3409e2edf034fe)



## Known Issues
There are issues with .ics files whose start dates contain timezone information.

