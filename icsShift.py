from datetime import datetime, date, timedelta
from icalendar import Calendar, Event, Alarm
import requests
import os

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
    daysList = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]
    
    
    startDateList = []
    endDateList = []
    #eventSummaryList = []
    #eventDescriptionList = []
    tzvalue = ""
    cal = Calendar.from_ical(data.read())
    rrules = []
    for component in cal.walk():
        if component.name == 'VCALENDAR':
            tzvalue = component.get('X-WR-TIMEZONE')
            break
    
    
    for event in cal.walk('vevent'):
        start = event.get('dtstart').dt
        
        startDateList.append(start)
        rrule = event.get('rrule')
        rrules.append(rrule)
        print(type(rrule))
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
    rruleCount = 0
    bigFile = ""
    for i in range(0, size):
        print(i, startDateList[i], newStartDateList[i], endDateList[i], newEndDateList[i])
    seenVEVENT = False
    
    with open(filename) as f:
        with open("answers.ics", "w") as f1:
            for line in f:
                # copies the file into another file line by line if the line contains a DTSTART or DTEND then the date will be replaced
                # also writes the file to a long string so that it can be returned and a user will have the opportunity to either copy and paste or download the file
                if "BEGIN:VEVENT" in line:
                    seenVEVENT = True
                if "RRULE" in line and seenVEVENT:
                    temp = line
                    if 'BYDAY' in line:
                        oldPart = temp[0:-3]
                        oldDay = temp[-3:-1]
                        val  = daysList.index(oldDay)
                        val+=dayOffset%7
                        newPart =daysList[val]
                        bigFile+=oldPart+newPart+'\n'
                        f1.write(oldPart+newPart+'\n')
                        continue
                if "DTSTART;VALUE" in line and seenVEVENT:
                    f1.write(
                        "DTSTART;VALUE=DATE:"+newStartDateList[count].strftime("%Y%m%d")+"\n")
                    bigFile += "DTSTART;VALUE=DATE:" + \
                        newStartDateList[count].strftime("%Y%m%d")+"\n"
                elif "DTSTART;TZID" in line and seenVEVENT:
                    f1.write("DTSTART;TZID="+tzvalue+":"+newStartDateList[count].strftime("%Y%m%d")+'T'+newStartDateList[count].strftime("%H%M%S")+'\n')
                    bigFile += "DTSTART;TZID="+tzvalue+":" + \
                        newStartDateList[count].strftime(
                            "%Y%m%d")+'T'+newStartDateList[count].strftime("%H%M%S")+'\n'
                elif "DTSTART:" in line and seenVEVENT:
                    f1.write(
                        "DTSTART:"+newStartDateList[count].strftime("%Y%m%d")+'T'+newStartDateList[count].strftime("%H%M%S")+'Z'+"\n")
                    bigFile += "DTSTART:" + \
                        newStartDateList[count].strftime(
                            "%Y%m%d") + 'T'+newStartDateList[count].strftime("%H%M%S")+'Z'+"\n"
                elif "DTEND;VALUE" in line and seenVEVENT:
                    f1.write(
                        "DTEND;VALUE=DATE:"+newEndDateList[count].strftime("%Y%m%d")+"\n")
                    bigFile += "DTEND;VALUE=DATE:" + \
                        newEndDateList[count].strftime("%Y%m%d")+"\n"
                    count+=1
                elif 'DTEND;TZID' in line and seenVEVENT:
                    f1.write('DTEND;TZID='+tzvalue+':'+newEndDateList[count].strftime('%Y%m%d')+'T'+newEndDateList[count].strftime('%H%M%S')+'\n')
                    bigFile += 'DTEND;TZID='+tzvalue+':' + \
                        newEndDateList[count].strftime(
                            '%Y%m%d')+'T'+newEndDateList[count].strftime('%H%M%S')+'\n'
                    count+=1
                elif "DTEND:" in line and seenVEVENT:
                    f1.write(
                        "DTEND:"+newEndDateList[count].strftime("%Y%m%d")+
                        'T'+newEndDateList[count].strftime("%H%M%S")+'Z'+"\n")
                    bigFile += "DTEND:"+newEndDateList[count].strftime("%Y%m%d")+'T'+newEndDateList[count].strftime("%H%M%S")+'Z'+"\n"
                    count+=1
                else:
                    f1.write(line)
                    bigFile+=line

    f.close()
    f1.close()
    if os.path.exists(filename):
        os.remove(filename)
    
    return bigFile


#print(main("6/18/2020", "/Users/sushruth/Downloads/otherCleanTest.ics"))

