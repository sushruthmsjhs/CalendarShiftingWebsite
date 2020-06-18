# Calendar Shifting

## Overview

The project is to take in any .ics file and a date that the user wishes to shift the first event to and return a modified .ics file with the shifted events and the same calendar details.

## Architecture

The application is implemented using python's flask framework. The application is also written with python and utilizes the icalendar and datetime packages

## Usage

1. Make sure python 3.5+ is installed on your machine
2. Clone or download the github repository located at https://github.com/sushruthmsjhs/CalendarShiftingWebsite
3. Navigate to the directory in terminal
4. Make sure that your python installation has the following packages installed. flask, requests, datetime, icalendar, wtforms (use pip3 install)
4. Run the controller.py file using python3 controller.py and open the url that shows up in terminal.

## Release

Version 1.1

- Fixed uploading multiple files issues
- Fixed rrules and timezone issues.

View the code at: https://github.com/sushruthmsjhs/CalendarShiftingWebsite

To use the application go to: https://calendar-shifting.herokuapp.com

## Known Issues

Recurring rules with more than one day per week, are not supported.
