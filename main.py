import csv
from math import sin, cos, sqrt, atan2, radians
from subprocess import Popen
import sys

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
f = open('data_short.csv')
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
    print("0. Exit Program")
    print("1. N/A")
    print("2. Request most popular start locations")
    print("3. Request most popular stop locations")
    print("4. What is the average distance traveled")
    print("5. Analyze ridership patterns (e.g. PassType, Duration)")
    print("6. Which locations require bike transport to maintain bike levels?")
    print("7. What is the breakdown of Trip Route Category-Passholder type combinations?")
    
    #call the input dialog box
    message = "What data do you desire?" #prompt 
    x = take_input(6, message, 0)

    #Cases: decide on the respective function based on integer input
    command = None
    command = sys.exit() if x == 0 else command
    command = sys.exit() if x == 1 else command
    command = most_popular_stations("Start") if x == 2 else command
    command = most_popular_stations("Stop") if x == 3 else command
    command = average_distance_traveled() if x == 4 else command
    command = sys.exit() if x == 5 else command
    command = sys.exit() if x == 6 else command
    command = sys.exit() if x == 7 else command
    
    command #call the decided function

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
        #extract the row's respective start orstop IDs
        loc_id = row[column]
        
        if loc_id not in popular_loc :   #if the data is not already in our dictionary of most popular IDs
            popular_loc[loc_id] = 1         #initialize it in the dictionary with the occurance as "1"
        else:                           #else:
            popular_loc[loc_id] += 1        #increment its occurance by 1

    #sort the popular ID dictionary into a list, organized in reverse order by the most visited stations
    popular_loc = sorted(popular_loc.items(), key=lambda kv: kv[1], reverse=True)

    #prompt for a quantity of desired location IDs
    message = "How many of the most popular stations do you want exported?"
    max_ans = len(popular_loc)
    min_ans = 0
    desired_quantity = take_input(max_ans, message, min_ans)

    #write the desired quantity of data to "output_filename"
    output_filename = 'Popular ' + start_stop + ' Locations.csv' #default filename
    output_filename = choose_filename(output_filename)           #allows user to specify unique filename
    columnheaders = ["Popular " + start_stop + " Locations", "Occurances"]
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
    except ZeroDivisionError:
        return_message1 = "All trips were round trips, no average"

    #write the desired quantity of data to "output_filename"
    output_filename = 'Average Distance Traveled.csv' #default filename
    output_filename = choose_filename(output_filename) #allows user to specify unique filename
    columnheaders = ["Average Distance Traveled (km)", "# of Round Trips Excluded", "Number of Blank Entries Excluded"]
    data_list = [[return_message1, return_message2, return_message3]]
    return_string = output_filename + " now has the average distance traveled stored!"
    desired_quantity = len(data_list)
    output_data(output_filename, columnheaders, data_list, return_string, desired_quantity)

#!!!!################## Secondary Input/Parsing Functions #######################!!!!#

#Dialog box maker, with checks in place
def take_input(max_ans, message, min_ans=0):
    print(message)

    #check if the input can be cast to an int. If it can't there was a bad input! Will need to re-enter data, however, it doesn't require a restart of the program, and informs the user
    try:
        ans = int(input("Must be integer within " + str(min_ans) + " and " + str(max_ans) + " inclusive: "))
    except ValueError:
        print("Invalid entry! Not integer!")
        ans = take_input(max_ans, message, min_ans)

    #checks if the value meets the quantity criteria
    if ans > max_ans or ans < min_ans: 
        print("Invalid entry!")
        ans = take_input(max_ans, message, min_ans)
    return ans

#File name chooser. Allows for custom filenames or to accept the default filename
def choose_filename(output_filename):
    #Take input of file name
    ans = input("Choose filename (including '.csv'). Press 'Enter' to accept default filename [" + output_filename + "]: ")

    #if the user chose the default filename by pressing enter, assign the default filename to ans
    if ans == "":
        ans = output_filename

    #checks if the choosen filename meets the criteria (.csv extension)     
    if '.csv' not in ans:
        print("Invalid entry! Needs '.csv' file extension!")
        ans = choose_filename(output_filename)

    return ans

#!!!!################## Data Export Functions #######################!!!!#

#Exports the data to .csv files, provided 5 arguments
def output_data(output_filename, columnheaders, data_list, return_string, desired_quantity = 0):
    #write the desired locations to "output_filename"
    i = 0
    tmp_storage = []
    tmp_storage.append(columnheaders) #Make first row of output CSV proper headers
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


#2a: Run command to find the most popular start locations
#most_popular_stations("Start")

#2b: run command to find the most popular stop locations
#most_popular_stations("Stop")

#3: run command to find the average distance traveled
#average_distance_traveled()
#p = Popen('Average Distance Traveled.csv', shell=True)

#4: Run command to find how many riders regularly commute via bikeshare?
# Calculate Monthly or Annual passes
#Flex pass: "Best if you expect to take two to four trips per month"
#Monthly pass: "Best if you expect to take five or more trips per month"
main_menu()