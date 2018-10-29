# Welcome to My Bikeshare Data Analyzer
Below is the documentation for my Python-coded bikeshare data analyzing script implemented for the [Capital One MindSumo Challenge](https://www.mindsumo.com/contests/bikeshare-data).

***
# 7 Primary Deliverables
### 1. Three Interesting Data Visuals
<img src="Github Pages/Graphs/1.jpg" width="500">

Pictured above is a graph of the average distance (in km) traveled in each of the 4 seasons. I selected this graph because I thought it was very interesting how drastic the drop in average distance traveled was for the Fall season. While I understood that Spring and Winter traveling distance would be lower, I didn't suspect that Fall would be as low as it was. I assumed it would be closer to Summer levels.

***
<img src="Github Pages/Graphs/2.jpg" width="500">

Pictured above is a graph of the number of bike pickups from all of the stations, with the x-axis (the station numbers) omitted). What I thought was most interesting were the 8 last stations. Over the course of July - March, **a 9 month period**, less than 200 bikes were picked up from each of these stations. Even at 191 bikes over 9 months, that still averages less than 1 bike a day being pulled.

***
<img src="Github Pages/Graphs/3.jpg" width="500">

Pictured above is a graph showing pass usage based on the season. I selected this graph because of two factors:
1. I realized that the Staff Annual pass did not have any riders in Spring and Summer, so I wonder if this pass was brought to fruition in the Fall of 2016.

2. I was suprised that the number of monthly pass rides is significantly lower in the Spring than the Winter. I would have thought that the Winter rides would have decreased compared to the Fall, while the Spring rides, as the weather improves and warms up, would see more riders than the Winter. However, the opposite was true, with Winter oddly being more popular than Spring.

***
### 2. Most popular stations

***
### 3. Average distance traveled

***
### 4. Regular bike commuters

***
### 5. Seasonal ridership trends

***
### 6. Net change in bikes

***
### 7. Route-passholder combos

`Talk about what combination would be more popular`
***
# Overview of Solution
### App and Main Menu
My analysis program consists of the three following files:
<br>
<img src="Github Pages/Main Menu/1.jpg" class="img-responsive" alt="">
1. **Data.csv** : This is the 35MB data file provided with the bikeshare data to be analyzed.
2. **Main.py** : This is my Python script file which will analyze the data.
3. **Bike Share Data Analyzer.bat** : This file, when ran, is responsible for running the Main.py file inside of a CMD prompt window. This allows for the program to be run independently of a compiler. As seen in later sceenshots, this greatly increases the ability to deploy this application without knowledge of how the code is working in the background or the knowledge of a compiler.

After the analyzer bat file is run, the python script will deploy, revealing the main menu interface to my application.
<img src="Github Pages/Main Menu/2.jpg" class="img-responsive" alt="">
There are 8 options to select from, ranging from 0 to 7, which are discussed in depth in the following sections.

Throughout my script, I have implemented protections against edge-case scenarios that would otherwise cause the program to crash and confuse the non-end user of this software. For example, trying to enter a number outside of 0 to 7 results in a message informing the user of this error. This input-guard functionality will be seen later in other aspects of the software.
<img src="Github Pages/Main Menu/3.jpg" class="img-responsive" alt="">

***
### Function 0
**Exit**
<img src="Github Pages/Function 0/1.jpg" class="img-responsive" alt="">
_The least exciting function to implement._ This function takes no input, simply closing the program.

***
### Function 1
**Most popular start stations**
<img src="Github Pages/Function 1/1.jpg" class="img-responsive" alt="">
Running function '1' will cause a prompt to appear, asking for how many of the most popular stations the user desires to have returned based on the number of unique stations in the dataset.
- After entering a desired quantity, the program then asks for a filename to export the analyzed data to.
- By just clicking 'Enter', the default filename displayed is chosen. Otherwise, the user can type their own custom filename.
- After deciding on a file name, the program prompts the user whether they wish to open the file or not.

<img src="Github Pages/Function 1/2.jpg" class="img-responsive" alt="">
Another place where input-guards has been implemented has been the filename selection prompt. All inputs must have a .csv data type extension, the extension must be at the end of the file name, and the file name must be longer than 4 characters (e.g., not just ".CSV").

<img src="Github Pages/Function 1/3.jpg" class="img-responsive" alt="">
<img src="Github Pages/Function 1/4.jpg" class="img-responsive" alt="">
Expanding on earlier, when prompted whether to open the file or not, selecting'Y' will open it in a spreadsheet program automatically (e.g., Excel), while selecting 'N' will..._well, not open it!_ This input is not case sensitive. Both 'Y' and 'N' have their own unique responses as show above, but both will then return to the main menu for further actions to be taken on the dataset.

<img src="Github Pages/Function 1/5.jpg" class="img-responsive" alt="" width="250"> <br>
Above is function 1's output data in the .csv file. There will be two columns, one denoting the station, and the other the number of pickups that occured at the dock. They are ordered by most popular, and in this case, we selected the top 10 start locations.

<img src="Github Pages/Function 1/6.jpg" class="img-responsive" alt="">
Furthermore, due to the program's CSV write functionality, if a user requests data and opens the CSV file, but then wishes to request more data and save it under the same filename without first closing the CSV file, the program will be unable to write to the file. Under normal circumstances, this would cause a program to crash due to a write error. However, my script is guarded against this behavior by checking if the file is open, and if it is, it prompts the user to close the file and click 'Enter' to resume the data write.

<img src="Github Pages/Function 1/7.jpg" class="img-responsive" alt="">
Finally, after the file has or has not been opened, the program automatically returns to the main menu. **All functions upon completion of exporting the data, return to the main menu automatically**

**It is worth mentioning at this point in the introduction that the guards and functionality of this function are primary to the program. These functionaltiies will, from now onward, be skimmed over for the following functions. All further sections will share similar guards such as write protection, input-guards for strings, dates, and integers when prompted, and the ability to open files after the data export is complete.**

***
### Function 2
**Most popular stop stations**
<img src="Github Pages/Function 2/1.jpg" class="img-responsive" alt="">

After running function 2, similar to most popular start locations, the program asks for the desired number of most popular stop locations, before saving them to a datasheet for viewing. Below is a copy of what is returned after requesting 10 most popular stop locations.

<img src="Github Pages/Function 2/2.jpg" class="img-responsive" alt="" width="250">

***
### Function 3
**Average distance traveled**
<img src="Github Pages/Function 3/1.jpg" class="img-responsive" alt="">

After running function 3, the code asks which file the data should be written to, and stores a CSV file with the following data format depicted below. Average distance was calculated by excluding round trips and entries where the Lat and Long coordinates were left blank. Mathematically, the function computes the Euclidean distance between the one-way trips and averages these routes. This only resulted in 9% of the data set being ignored for average distance calculations, as I did not wish to assume bikers were biking the whole duration of a ride at a given speed and overestimate distance.

<img src="Github Pages/Function 3/2.jpg" class="img-responsive" alt="" width="550">

***
### Function 4
**Regular bike commuters**
<img src="Github Pages/Function 4/1.jpg" class="img-responsive" alt="">

After running function 4, the code asks which file the data should be written to, and stores an CSV file with the following data format depicted below. The code assumes that only monthly and annual pass rides are "regular" commutes, due to the provided defintions on the bikeshare data website for walk-up and flex-pass. This CSV file stores the raw quantity of monthly pass rides and annual pass rides, as well as the sum of ALL rides. It then uses this data to compute percentages to accompany the raw numerical data.

<img src="Github Pages/Function 4/2.jpg" class="img-responsive" alt="" width="600">

***
### Function 5
**Seasonal ridership trends**
<img src="Github Pages/Function 5/1.jpg" class="img-responsive" alt="">

After running function 5, the entries of the data set are split into 4 meterological seasons:
* Spring
* Summer
* Fall
* Winter

After branching the data, operations are performed on these seasonal subsets of the whole data set. These functions include:
* Average distance traveled (in km)
* Average commute time (in minutes)
* Total number of rides
* Total rides based on the pass type

The data is then arranged and output in the following format based on season:

<img src="Github Pages/Function 5/2.jpg" class="img-responsive" alt="">

***
### Function 6
**Net change in bikes**
<img src="Github Pages/Function 6/1.jpg" class="img-responsive" alt="">

After running function 6, the user is prompted to enter a date, including day, month, and year. Similarly, this function has guards on both month and day entries, and if the date selected has no data entries, it informs the user as shown above, with a message stating there is not data for the avaialable date. It then returns to the main menu.

However, provided that a desired date for analysis is selected which has data, the function will return two stations' data:
1. The station which most desperately requires more bikes be added
2. The station which most desperately requires bikes to be removed

There were several ways in which this priority could be calculated. I chose to have my function analyze all stations and their hourly net change of bikes by summing the bikes leaving and arriving at a station for every given hour of the desired day. After sorting this list in reverse descending order, the station with an hour containing the largest negative or positive delta of bikes for any given hour took priority for either needing bike replenishment or removal respectively.

The function then outputs two graphs depicted below. The first graph displays the station number and an hourly graph of the net change in bikes for that day, stating that bikes need to be added. This graph can be saved or manipulated using the controls on the graph window. Its also worth noting that a bar graph y-value of zero implies no net change in bikes for that hour.

<img src="Github Pages/Function 6/2.jpg" class="img-responsive" alt="">

After the first graph is closed, the second graph is generated automatically, showing an hourly graph of the net change in bikes for that day at the denoted station, stating that bikes need to be removed.

<img src="Github Pages/Function 6/3.jpg" class="img-responsive" alt="">

***
### Function 7
**Trip route category-passholder combos**
<img src="Github Pages/Function 7/1.jpg" class="img-responsive" alt="">

After running function 7, the program asks for a desired filename, before saving them to a datasheet for viewing. The output CSV file sorts the data into Round Trip and One Way trip categories. Then, it sums then number of rides for each passholder which occured under each trip category. Below is a copy of what is returned for our dataset.

<img src="Github Pages/Function 7/2.jpg" class="img-responsive" alt="" width="600">
