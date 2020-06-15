from datetime import datetime, date, timedelta
from icalendar import Calendar, Event, Alarm
import requests


#Calculate the Days between Two Dates

def differ_days(date1, date2):
    a = date1
    b = date2
    return(b-a).days

#the main method that performs the operation of shifting start and end dates. 
# It returns a string so the user can easily copy paste it
def main(r, filename):
    data = open(filename, 'rb') #opens a file to read gets from controller.py
    
    newStart = datetime.strptime(r, "%m/%d/%Y").date() # strips the input string for the specific month day and year values
    #print(newStart)
    minDate = date(9999, 12, 31) # the maximum possible allowed date all start dates have to be less than this date
    startDateList = []
    endDateList = []
    #eventSummaryList = []
    #eventDescriptionList = []
    cal = Calendar.from_ical(data.read())

    print(minDate)
    for event in cal.walk('vevent'):
        start = event.get('dtstart').dt
        
        startDateList.append(start)
        if(isinstance(start, datetime)):
            newStartDate = date(start.year, start.month, start.day)
        else:
            newStartDate = start
        #print('type newStartDate', type(newStartDate))
        #print('type startDate', type(start))
        #print('type minDate', type(minDate))
        if(newStartDate < minDate):
            minDate = newStartDate
        end = event.get('dtend').dt
        endDateList.append(end)
    newStartDateList = []
    newEndDateList = []
    print("minDate", minDate)
    print("new start", newStart)
    dayOffset = differ_days(minDate, newStart)
    print("offset", dayOffset)
    size = len(startDateList)
    print('size', size)
    for i in range(0, size):
        startDate = startDateList[i]
        # adds the number of offset days to generate a new start date
        newStartDate = startDate + timedelta(days=dayOffset)
        endDate = endDateList[i]

        newEndDate = endDate + timedelta(days=dayOffset)
        newStartDateList.append(newStartDate)
        newEndDateList.append(newEndDate)
    count = 0
    bigFile = ""
    print('size', len(newStartDateList))
    with open(filename) as f:
        with open("answers.ics", "w") as f1:
            for line in f:
                # copies the file into another file line by line if the line contains a DTSTART or DTEND then the date will be replaced
                # also writes the file to a long string so that it can be returned and a user will have the opportunity to either copy and paste or download the file
                if "DTSTART;VALUE" in line:
                    f1.write(
                        "DTSTART;VALUE=DATE:"+newStartDateList[count].strftime("%Y%m%d")+"\n")
                    bigFile += "DTSTART;VALUE=DATE:" + \
                        newStartDateList[count].strftime("%Y%m%d")+"\n"
                elif "DTSTART:" in line:
                    f1.write(
                        "DTSTART:"+newStartDateList[count].strftime("%Y%m%d%H%M%S")+"\n")
                    bigFile += "DTSTART:" + \
                        newStartDateList[count].strftime(
                            "%Y%m%d%H%M%S")+"\n"
                elif "DTEND;VALUE" in line:
                    f1.write(
                        "DTEND;VALUE=DATE:"+newEndDateList[count].strftime("%Y%m%d")+"\n")
                    bigFile += "DTEND;VALUE=DATE:" + \
                        newEndDateList[count].strftime("%Y%m%d")+"\n"
                    count+=1
                elif "DTEND" in line:
                    f1.write(
                        "DTEND:"+newEndDateList[count].strftime("%Y%m%d%H%M%S")+"\n")
                    bigFile += "DTEND:" + \
                        newEndDateList[count].strftime("%Y%m%d%H%M%S")+"\n"
                    count+=1
                else:
                    f1.write(line)
                    bigFile+=line

    f.close()
    f1.close()
    return bigFile
#print(main("7/20/2020", "testCalendar.ics"))

