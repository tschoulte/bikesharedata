import csv
from math import sin, cos, sqrt, atan2, radians
from subprocess import Popen
import matplotlib.pyplot as plt
from datetime import datetime
from operator import itemgetter
import numpy as np

#initialization of the indices of the excel columns
tripID, duration = 0, 1
startTime, endTime = 2, 3
sStatID, sStatLat, sStatLon = 4, 5, 6
eStatID, eStatLat, eStatLon = 7, 8, 9
bikeID = 10
pDuration = 11
tripCat, passType = 12, 13
startLatLong, endLatLong = 14, 15

#open csv file
f = open('data.csv') #change data source here quickly
csv_f = csv.reader(f)

#import csv file into a list of lists. Remove the header row
data = []
for row in csv_f:
  data.append(row)
data.pop(0)

#!!!!############### Main Menu ##########################!!!!#
#Function: Main Menu
def main_menu():
    #print the main command options
    print("-----------------------------------------------------------------")
    print("0. Exit Program")
    print("1. Request most popular start locations")
    print("2. Request most popular stop locations")
    print("3. What is the average distance traveled")
    print("4. How many riders include bike sharing regularly?")
    print("5. Analyze seasonal trends (e.g. PassType, Duration)")
    print("6. Which locations require bike transport to maintain bike levels?")
    print("7. What is the breakdown of Trip Route Category-Passholder type combinations?")
    
    #call the input dialog box
    print('')
    message = "Which function/data do you desire?" #prompt 
    x = take_numerical_input(7, message, 0)
    print('')

    #Cases: decide on the respective function based on integer input
    command = None
    command = exit if x == 0 else command
    command = most_popular_stations("Start") if x == 1 else command
    command = most_popular_stations("Stop") if x == 2 else command
    command = average_distance_traveled() if x == 3 else command
    command = regular_commuters() if x == 4 else command
    command = seasonal_trends() if x == 5 else command
    command = bike_transport() if x == 6 else command
    command = trip_passholder_combos() if x == 7 else command
    
    if command == exit:
        print('Exiting. Have a nice day!')

#!!!!################## Primary Functions #######################!!!!#

#Function 2: Request most popular start or stop locations
def most_popular_stations(start_stop):
    popular_loc = {} #create dictionary of most popular start or stop location IDs

    #assign the appropriate column based on request 
    if start_stop == "Start":
        column = sStatID
    elif start_stop == "Stop":
        column = eStatID

    for row in data: #for each row in the dataset
        #extract the row's respective start or stop IDs
        loc_id = row[column]
        
        if loc_id not in popular_loc :   #if the data is not already in our dictionary of most popular IDs
            popular_loc[loc_id] = 1         #initialize it in the dictionary with the occurrence as "1"
        else:                           #else:
            popular_loc[loc_id] += 1        #increment its occurrence by 1

    #sort the popular ID dictionary into a list, organized in reverse order by the most visited stations
    popular_loc = sorted(popular_loc.items(), key=lambda kv: kv[1], reverse=True)

    #prompt for a quantity of desired location IDs
    message = "How many of the most popular stations do you want exported?"
    max_ans = len(popular_loc)
    min_ans = 0
    desired_quantity = take_numerical_input(max_ans, message, min_ans)

    #write the desired quantity of data to "output_filename"
    output_filename = 'Popular ' + start_stop + ' Locations.csv' #default filename
    output_filename = choose_filename(output_filename)           #allows user to specify unique filename
    columnheaders = ["Popular " + start_stop + " Locations", "Occurrences"]
    data_list = popular_loc
    return_string = output_filename + " now has the " + str(desired_quantity) + " most popular " + start_stop.lower() + " locations."
    output_data(output_filename, columnheaders, data_list, return_string, desired_quantity)

#Function 3: Find the average distance traveled
def average_distance_traveled():
    R = 6373.0 # approximate radius of earth in km
    total_distance = 0 #sum of all valid distances
    num_rows = 0 #used for dividing sum of distance for average distance. Excludes round_trip_counter and blank_counter
    round_trip_counter = 0 #count number of round trips (because distance for a round trip is 0km)
    blank_counter = 0 #count number of empty-rows for start or stop location. These shouldn't be included

    for row in data: #for each row in the dataset
        if row[tripCat] == "One Way": #only include one-ways, as round-trips have a distance traveled of 0
            if (row[sStatLat] and row[sStatLon] and row[eStatLat] and row[eStatLon]) != "": #if the start or stop lon/lat's contain data, calculate
                num_rows += 1
                #extract the row's lat's and lon's
                lat1 = radians(float(row[sStatLat]))
                lon1 = radians(float(row[sStatLon]))
                lat2 = radians(float(row[eStatLat]))
                lon2 = radians(float(row[eStatLon]))

                #Compute deltas
                delta_lon = lon2 - lon1
                delta_lat = lat2 - lat1

                #Calculate distance
                a = sin(delta_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = R*c
                total_distance += distance

            else: #if the start or stop lon/lat's don't contain data, increment blank_counter
                blank_counter += 1

        else: #if the trip is a round trip, increment round_trip_counter
            round_trip_counter += 1
    
    #parse messages we will return
    return_message2 = str(round_trip_counter)
    return_message3 = str(blank_counter)
    try:
        ans = total_distance/num_rows
        return_message1 = str(round(ans, 2))
    except ZeroDivisionError: #avoid dividing by zero if all trips were round-trip
        return_message1 = "All trips were round trips, no average"

    #write the desired quantity of data to "output_filename"
    output_filename = 'Average Distance Traveled.csv' #default filename
    output_filename = choose_filename(output_filename) #allows user to specify unique filename
    columnheaders = ["Average Distance Traveled (km)", "# of Round Trips Excluded", "Number of Blank Entries Excluded"]
    data_list = [[return_message1, return_message2, return_message3]]
    return_string = output_filename + " now has the average distance traveled stored!"
    desired_quantity = len(data_list)
    output_data(output_filename, columnheaders, data_list, return_string, desired_quantity)

#4: Run command to find how many riders regularly commute via bikeshare
# Calculate sum of Monthly or Staff Annual passes
#Flex pass: "Best if you expect to take two to four trips per month", so not regular
#Monthly pass: "Best if you expect to take five or more trips per month", quantifies as regular
def regular_commuters():
    column = passType

    #keep track of occurrences in [[Monthly Pass #, Staff Annual Pass #]]
    regular_commuters = [["Quantity", 0, 0, 0]
                        ,["Total Percent of ALL Rides:", 0, 0, 0]]
    total_commutes = 0

    for row in data: #for each row in the dataset
        #extract the row's respective Pass Type
        pass_value = row[column]
        total_commutes += 1 #total of all commutes

        if pass_value == "Monthly Pass":
            regular_commuters[0][1] += 1    #increment Monthly Pass occurrence by 1
        if pass_value == "Staff Annual":
            regular_commuters[0][2] += 1    #increment Annual Pass occurrence by 1
    
    #Calculate the total number of regular commuters
    regular_commuters[0][3] = regular_commuters[0][1] + regular_commuters[0][2]

    #Calculate Row 2's percentages
    regular_commuters[1][1] = "{:.2%}".format(regular_commuters[0][1]/total_commutes)
    regular_commuters[1][2] = "{:.2%}".format(regular_commuters[0][2]/total_commutes)
    regular_commuters[1][3] = "{:.2%}".format((regular_commuters[0][1] + regular_commuters[0][2])/total_commutes)

    #write the desired quantity of data to "output_filename"
    output_filename = 'Regular Commuters.csv' #default filename
    output_filename = choose_filename(output_filename)           #allows user to specify unique filename
    columnheaders = ["", "Monthly Pass Rides", "Staff Annual Pass Rides", "Total Regular Rides"]
    data_list = regular_commuters
    return_string = output_filename + " now stores data on regular commuters."
    desired_quantity = len(data_list)
    output_data(output_filename, columnheaders, data_list, return_string, desired_quantity)

#5:How does ridership change with seasons? Types of passes used, trip duration, etc
#Meterological Seasons: Spring: March-May (3-5), Summer: June-August (6-8), Fall: September-November (9-11), Winter: December-February (12,1,2)
def seasonal_trends():
    spring = [] #hold data for our given season
    summer  = []
    fall = []
    winter = []

    for row in data: #for each row in the dataset
        #extract date and put it into list if it matches our desired date
        datetime_start = datetime.strptime(row[startTime], '%Y-%m-%dT%H:%M:%S') #datetime object for drop-off 
        datetime_end = datetime.strptime(row[endTime], '%Y-%m-%dT%H:%M:%S') #datetime object for drop-off 
        pass_type = row[passType]
        month = datetime_start.month

        #if the desired month is the in the range of our season, append the data row to this season's data
        #                    0            1               2           3               4               5         6 (START TIME) 7 (STOP TIME)      8           9 
        station_info = [row[sStatID], row[sStatLat], row[sStatLon], row[eStatID], row[eStatLat], row[eStatLon], datetime_start, datetime_end, pass_type, row[tripCat]]
        if 3 <= month <= 5:     #Spring
            spring.append(station_info)   #add the data to the season's list
        elif 6 <= month <= 8:   #Summer
            summer.append(station_info)   #add the data to the season's list
        elif 9 <= month <= 11:  #Fall
            fall.append(station_info)   #add the data to the season's list 
        else:                   #Winter
            winter.append(station_info)   #add the data to the season's list
    
    
    #At this point, we have our data that fits our date in four unorganized lists:
    #Spring, Summer, Fall, and Winter
    annual_seasons = [spring, summer, fall, winter]
    i = 0
    final_ans = [["Spring"],["Summer"],["Fall"],["Winter"]]
    for season in annual_seasons:
        

    #average distance
        R = 6373.0 # approximate radius of earth in km
        total_distance = 0 #sum of all valid distances
        num_rows = 0 #used for dividing sum of distance for average distance. Excludes round_trip_counter and blank_counter
        round_trip_counter = 0 #count number of round trips (because distance for a round trip is 0km)
        blank_counter = 0 #count number of empty-rows for start or stop location. These shouldn't be included

        for trip in season: #for each row in the dataset
            if trip[9] == "One Way": #only include one-ways, as round-trips have a distance traveled of 0
                if (trip[1] and trip[2] and trip[4] and trip[5]) != "": #if the start or stop lon/lat's contain data, calculate
                    num_rows += 1
                    #extract the row's lat's and lon's
                    lat1 = radians(float(trip[1]))
                    lon1 = radians(float(trip[2]))
                    lat2 = radians(float(trip[4]))
                    lon2 = radians(float(trip[5]))

                    #Compute deltas
                    delta_lon = lon2 - lon1
                    delta_lat = lat2 - lat1

                    #Calculate distance
                    a = sin(delta_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2)**2
                    c = 2 * atan2(sqrt(a), sqrt(1 - a))
                    distance = R*c
                    total_distance += distance

                else: #if the start or stop lon/lat's don't contain data, increment blank_counter
                    blank_counter += 1

            else: #if the trip is a round trip, increment round_trip_counter
                round_trip_counter += 1

        try:
            ans = total_distance/num_rows
            return_message1 = str(round(ans, 2)) + " km"
        except ZeroDivisionError: #avoid dividing by zero if all trips were round-trip
            return_message1 = "Only Round Trips/No Data"
        final_ans[i].append(return_message1)

    #avg duration
        total_time = 0 #sum of all valid distances
        num_rows = 0 #used for dividing sum of distance for average distance. Excludes round_trip_counter and blank_counter

        for trip in season: #for each row in the dataset
            start_time = trip[6]
            end_time = trip[7]
            if (start_time and end_time) != "": #if the start or stop lon/lat's contain data, calculate
                num_rows += 1
                #calculate delta in time between docking and undocking (in minutes)
                minute_delta = (end_time - start_time).seconds / 60

                total_time += minute_delta

            else: #if the start or stop lon/lat's don't contain data, increment blank_counter
                blank_counter += 1

        try:
            ans = total_time/num_rows
            return_message1 = str(round(ans, 1)) + " minutes"
        except ZeroDivisionError: #avoid dividing by zero if no trips
            return_message1 = "No Data"
        final_ans[i].append(return_message1)
        
        pass_type_sums = [0,0,0,0,0]
    #check # of passes of each type used.
        for trip in season: #for each row in the dataset
            pass_value = trip[8]
            

            if pass_value == "Staff Annual":
                pass_type_sums[4] += 1 #total of all commutes
                pass_type_sums[0] += 1    #increment Monthly Pass occurrence by 1
            if pass_value == "Monthly Pass":
                pass_type_sums[4] += 1 #total of all commutes
                pass_type_sums[1] += 1    #increment Annual Pass occurrence by 1
            if pass_value == "Flex Pass":
                pass_type_sums[4] += 1 #total of all commutes
                pass_type_sums[2] += 1    #increment Annual Pass occurrence by 1
            if pass_value == "Walk-up":
                pass_type_sums[4] += 1 #total of all commutes
                pass_type_sums[3] += 1    #increment Annual Pass occurrence by 1

        final_ans[i].append(pass_type_sums)
        i += 1
    
    data_list = []
    for season in final_ans:
        data_list.append([season[0],season[1],season[2],season[3][4],season[3][0],season[3][1],season[3][2],season[3][3]])
    #write the desired quantity of data to "output_filename"
    output_filename = 'Seasonal Trends.csv' #default filename
    output_filename = choose_filename(output_filename)           #allows user to specify unique filename
    columnheaders = ["Season", "Average Distance Traveled", "Average Commute Time", "Total Number of Rides", "Total Annual Pass Rides", "Total Month Pass Rides", "Total Flex Pass Rides", "Total Walk-Up Rides"]
    data_list = data_list
    return_string = output_filename + " now stores data on seasonal trends."
    desired_quantity = len(data_list)
    output_data(output_filename, columnheaders, data_list, return_string, desired_quantity)


#6: Which locations require bike transport to maintain bike levels?
def bike_transport():
    #original dataset dates: 7/7/2016 - 3/31/2017
    #Allow user to select a date
    print("You need to select a day to analyze bike data!")
    message = "Enter integer day (1-31): "
    day = take_numerical_input(31, message, 1)
    message = "Enter integer month (1-12): "
    month = take_numerical_input(12, message, 1)
    message = "Enter integer year (YYYY): "
    year = input(message)
    desired_date = str(month) + "/" + str(day) + "/" + year
    print("You have chosen " + desired_date + ".")
    desired_date = datetime.strptime(desired_date, '%m/%d/%Y')

    arrivals = [] #hold drop-offs for our given day
    departures = [] #hold pick-ups for our given day
    for row in data: #for each row in the dataset
        #extract date and put it into list if it matches our desired date
        datetime_arrival = row[endTime] #raw date/time string
        datetime_depart = row[startTime] #raw date/time string
        datetime_arrival = datetime.strptime(datetime_arrival, '%Y-%m-%dT%H:%M:%S') #datetime object for drop-off
        datetime_depart = datetime.strptime(datetime_depart, '%Y-%m-%dT%H:%M:%S') #datetime object for pick-up

        #if the desired date is the same as our drop-off/pickup time, append it to 'arrivals' or 'departures' as data we should analyze
        #append the data in the format ["StationID", timestamp of drop-off/pickup]
        if datetime_arrival.date() == desired_date.date():
            station_info = [row[eStatID], datetime_arrival]
            arrivals.append(station_info)   #increment its occurrence by 1
        if datetime_depart.date() == desired_date.date():
            station_info = [row[sStatID], datetime_depart]
            departures.append(station_info)   #increment its occurrence by 1

        #Since our dataset is quite large, and since our data is in chronological order in rows
        #if we reach a date where it is LATER than our desired date, we can break and end
        #our search early to save compute time
        if datetime_depart.date() > desired_date.date():
            break
    
    #At this point, we have our data that fits our date in two unorganized lists:
    #'Arrivals' and 'Departures'
    #This section sorts our data into a series of nested dictionaries in the following format:
    # arrivals = {{Hour1: {StationID1: Total # of Arrivals during Hour1, StationID2 : Total # of Arrivals during Hour1, ...}
    #            ,{Hour2: {StationID1: Total # of Arrivals during Hour2, StationID2 : Total # of Arrivals during Hour2, ...}
    #            ,{Hour3: {StationID1: Total # of Arrivals during Hour3, StationID2 : Total # of Arrivals during Hour3, ...} 
    #            , {.....} }
    timeIntervals_net = {} #this will store our net arrivals/departures

    #*******First, add the arrivals to the dictionary. Every station will have a positive or 0 value after this step for each provided hour
    for entry in arrivals: #for each arrival
        hour = entry[1].hour   #extract its hour of drop-off
        station = entry[0]     #extract the stationID string

        if hour not in timeIntervals_net:   #if the hour is not already entered into the timeIntervals_net
            timeIntervals_net[hour] = {station : 1} #Add the single station dictionary with a value of 1
        elif station not in timeIntervals_net[hour]:    #If the stationID is not inside of the nested hour dictionary
            timeIntervals_net[hour][station] = 1        #Add the station with a value of 1
        else:                                  #if the station already exists for that given hour:
            timeIntervals_net[hour][station] += 1   #Increment its value by 1 arrival

    #*******Second, subtract the departures from the dictionary. This will give us a net flow per each hour
    for entry in departures: #for each departure
        hour = entry[1].hour    #extract its hour of pick-up
        station = entry[0]      #extract the stationID string

        if hour not in timeIntervals_net:   #if the hour is not already entered into the timeIntervals_net
            timeIntervals_net[hour] = {station : -1}    #Add the single station dictionary with a value of -1 (because it was taken away from the dock)
        elif station not in timeIntervals_net[hour]:    #If the stationID is not inside of the nested hour dictionary
            timeIntervals_net[hour][station] = -1       #Add the station with a value of -1
        else:                                   #if the station already exists for that given hour:
            timeIntervals_net[hour][station] -= 1   #Decrement its value by 1 arrival

    remove_bikes = ["", float("-inf"), ]
    add_bikes = ["", float("inf"), ]
    for hour, station in timeIntervals_net.items():
        #print("\Hour:", hour)
        for stationID in station:
            #print(stationID + ':', station[stationID])
            if station[stationID] > remove_bikes[1]:
                remove_bikes = [stationID, station[stationID], hour]
            if station[stationID] < add_bikes[1]:
                add_bikes = [stationID, station[stationID], hour]

    add_bikes_x_axis = {}
    remove_bikes_x_axis = {}
    #using the above stations, we will now graph their hourly net trends over a day
    for hour, station in timeIntervals_net.items():
        for stationID in station:
            if stationID == add_bikes[0]:
                add_bikes_x_axis[hour] = station[stationID]
            if stationID == remove_bikes[0]:
                remove_bikes_x_axis[hour] = station[stationID]

    #calls the graphing function to graph the hourly data about the station that needs more bikes and the station that needs bikes removed
    plot_title = 'Station ' + add_bikes[0] + ": Needs Bikes Added"
    graph_station(add_bikes_x_axis, add_bikes[0], plot_title)

    plot_title = 'Station ' + remove_bikes[0] + ": Needs Bikes Removed"
    graph_station(remove_bikes_x_axis, remove_bikes[0], plot_title)

    main_menu()

#7: What is the breakdown of Trip Route Category-Passholder type combinations? What might make a particular combination more popular?
def trip_passholder_combos():
    exit

#!!!!################## Secondary Input/Parsing Functions #######################!!!!#

#Dialog box maker, with checks in place. Integers only!
def take_numerical_input(max_ans, message, min_ans=0):
    print(message)

    #check if the input can be cast to an int. If it can't there was a bad input! Will need to re-enter data, however, it doesn't require a restart of the program, and informs the user
    try:
        ans = int(input("Must be integer within " + str(min_ans) + " and " + str(max_ans) + " inclusive: "))
    except ValueError:
        print("Invalid entry! Not integer!")
        ans = take_numerical_input(max_ans, message, min_ans)

    #checks if the value meets the quantity criteria
    if ans > max_ans or ans < min_ans: 
        print("Invalid entry!")
        ans = take_numerical_input(max_ans, message, min_ans)
    return ans

#File name chooser. Allows for custom filenames or to accept the default filename
def choose_filename(output_filename):
    #Take input of file name
    print('')
    print("Type desired filename (including '.csv').")
    ans = input("Press 'Enter' to accept default filename [" + output_filename + "]: ")

    #if the user chose the default filename by pressing enter, assign the default filename to ans
    if ans == None or ans == "":
        ans = output_filename

    #checks if the choosen filename meets the criteria (5+ characters and .csv extension)     
    x = len(ans) #length of entered filename

    #the shotest possible file name is 5 characters
    if x < 5:
        print("Invalid entry!")
        ans = choose_filename(output_filename)
        return ans

    extension = ans[x-4:x] #checks last 4 characters to ensure .csv extension type
    if extension != '.csv':
        print("Invalid entry (no '.csv' extension)!")
        ans = choose_filename(output_filename)
        return ans
    return ans
    
#!!!!################## Data Export Functions #######################!!!!#

#Exports the data to .csv files, provided 5 arguments
def output_data(output_filename, columnheaders, data_list, return_string, desired_quantity = 0):
    #write the desired locations to "output_filename"
    i = 0
    tmp_storage = []
    tmp_storage.append(columnheaders) #Make first row of output CSV proper headers
    try:   
        with open(output_filename, 'w') as myfile:
            writer = csv.writer(myfile, lineterminator = '\n')
            while i < desired_quantity:     #While there is still more desired data to write
                #Handles the limited edge-case scenarios where a data cell is empty,
                #Reassigning it from a blank ID to one stating "Data Not Provided" in the output CSV
                #Code is functional without it, but is more informative to the non-end user looking at resultant data
                if str(data_list[i][0]) == "":
                    tmp_storage.append(["Data Not Provided", data_list[i][1]]) #add data to the temp output list, with above mentioned twist
                else:
                    tmp_storage.append(data_list[i]) #add data to the temp output list
                i += 1
            writer.writerows(tmp_storage) #writes all the added data to the CSV
        print(return_string) #Informs the user where the data went/that operations were successful
        print('')
        open_file(output_filename)
    except PermissionError:
        x = input('Sorry, please close ' + output_filename + ' and then press Enter >>>')
        output_data(output_filename, columnheaders, data_list, return_string, desired_quantity)

def open_file(output_filename):
    print("Would you like to open the file now?")
    x = input("Type 'Y' or 'N' >>> ")
    if isinstance(x, str) == False:
        print("Invalid entry! Please only type Y or N, no quotes")
        open_file(output_filename)

    if x.lower() == "y":
        Popen(output_filename, shell=True)
        print(output_filename + " has been opened!")
    elif x.lower() == "n":
        print("Not opening it. No problem!")
    else:
        print("Invalid entry! Please only type Y or N, no quotes")
        print('')
        open_file(output_filename)

    print('Hope that helped! Sending you to the main menu now!')
    print('')
    main_menu()

def graph_station(x_axis, station, plot_title):
    # heights of bar graphs
    red_height = []
    green_height = []


    #Populate red_height for bikes lost, populate green_height for bikes gained
    i = 0
    while i < 24:
        x1 = x_axis.get(i, 0)
        if x1 < 0:
            red_height.append(x1)
            green_height.append(0)
        else:
            red_height.append(0)
            green_height.append(x1) 
        i += 1
    
    #If the net change for every single bicycle station for every single hour
    #of a desired day is ZERO, then there is no data for that day.
    #The user should be informed of this anomaly, and returned to the main menu
    all_heights = [red_height, green_height] #all of our Y-Axis values for the graph
    data = False
    for height_list in all_heights: #for each of the 2 lists
        for entry in height_list: #for each Y-value
            if entry != 0: #if it's not zero, then we have valid data
                data = True
    if data == False: #If no data was found for this day, notify the user and return to the main menu
        print('')
        print("No data is available for that date! Returning you to the main menu.")
        main_menu() #return to the main menu
        return

    #x-axis coordinates
    left = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    #Labels for bars on x-axis
    tick_label = ['12AM','','','3AM','','','6AM','','','9AM','','','12PM',
                  '','','3PM','','','6PM','','','9PM','','11PM']

    #Plot Graph
    plt.bar(left, green_height, tick_label = tick_label, width = 0.4, color = 'green') 
    plt.bar(left, red_height, tick_label = tick_label, width = 0.4, color = 'red')
    #Give Graph some characteristics
    plt.xlabel('Time of Day (Hours)') 
    plt.ylabel('Net Change in Bikes (Negative -> Loss, Positive -> Gain') #Label y-axis 
    plt.title(plot_title) # plot title 
    plt.show() #Show Graph

main_menu()