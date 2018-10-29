# Welcome to My Bikeshare Data Analyzer
Below is the documentation for my Python-coded bikeshare data analyzing script implemented for the [Capital One MindSumo Challenge](https://www.mindsumo.com/contests/bikeshare-data).
## 7 Primary Deliverables
### 3 Data Visuals
<img src="Github Pages/Graphs/1.jpg" width="500">
<br>
Pictured above is a graph of the average distance (in km) traveled in each of the 4 seasons. I selected this graph because I thought it was very interesting how drastic the drop in average distance traveled was for the Fall season. While I understood that Spring and Winter would be lower, I didn't suspect that Fall would be as low as it was. I assumed it would be closer to Summer levels.

<img src="Github Pages/Graphs/2.jpg" width="500">
<br>
Pictured above is a graph of the number of bike pickups from all of the stations, with the x-axis (the station numbers) omitted). What I thought was most interesting were the 8 last stations. All of these stations, over the course of July - March, **a 9 month period**, less than 200 bikes were picked up from these stations. Even at 191 bikes over 9 months, that still averages less than 1 bike a day being pulled.
<img src="Github Pages/Graphs/3.jpg" width="500">
<br>
Pictured above is a graph showing pass usage based on the season. I selected this graph because of two factors:
1. I realized that the Staff Annual pass did not have any riders in Spring and Summer, so I wonder if this pass was brought to fruition in the Fall of 2016.
2. I was surprised that the number of monthly pass rides is significantly lower in the Spring than the Winter. I would have thought that the Winter rides would have decreased, while the Spring rides, as the weather improves and warms up, would see more riders. However, the opposite was true, with Winter being more popular than Spring.

## Overview of Solution
### App and Main Menu
The analysis program consists of the three following files:
<br>
<img src="Github Pages/Main Menu/1.jpg" class="img-responsive" alt="">
1. **Data.csv** : This is the 35MB data file provided with the bikeshare data to be analyzed.
2. **Main.py** : This is my Python script file which will analyze the data.
3. **Bike Share Data Analyzer.bat** : This file, when ran, is responsible for running the Main.py file inside of a CMD prompt window. This allows for the program to be run independently of a compiler. As seen in later sceenshots, this greatly increases the ability to deploy this application without knowledge of how the code is working in the background or the knowledge of a compiler.

After the analyzer bat file is run, the python script will deploy, revealing the main menu interface to my application.
<img src="Github Pages/Main Menu/2.jpg" class="img-responsive" alt="">
There are 8 options to select from, ranging from 0 to 7.

Throughout my script, I have implemented protections against edge-case scenarios that would otherwise cause the program to crash and confuse the non-end user of this software. For example, trying to enter a number outside of 0 to 7 results in a message informing the user of this error. This input-guard functionality will be seen later in other aspects of the software.
<img src="Github Pages/Main Menu/3.jpg" class="img-responsive" alt="">

### Function 0: Exit
<img src="Github Pages/Function 0/1.jpg" class="img-responsive" alt="">
_The least exciting function to implement._ This function takes no input, simply closing the program.

### Function 1: Which start stations are most popular?
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
Above is the output data in the .csv file. There will be two columns, one denoting the station, and the other the number of pickups that occured at the dock. They are ordered by most popular, and in this case, we selected the top 10 start locations.

<img src="Github Pages/Function 1/6.jpg" class="img-responsive" alt="">
Furthermore, due to the program's CSV write functionality, if a user requests data, and opens the CSV file, and then wants to request more data and save it under the same filename without first closing the CSV file, the program will be unable to write to the file. Under normal circumstances, this would cause a program to crash due to a write error. However, my script is guarded against this behavior by checking if the file is open, and if it is, it prompts the user to close the file and click 'Enter' to resume the data write.

<img src="Github Pages/Function 1/7.jpg" class="img-responsive" alt="">
Finally, after the file has or has not been opened, the program automatically returns to the main menu.

**It is worth mentioning at this point in the introduction that the primary guards and functionality of the program has been described in this section. All further sections will share similar guards such as write protection, input-guards for strings, dates, and integers when prompted, and the ability to open files after the data export is complete.**

### Function 2: Which stop stations are most popular?
<img src="Github Pages/Function 2/1.jpg" class="img-responsive" alt="">
<img src="Github Pages/Function 2/2.jpg" class="img-responsive" alt="" width="250">

### Function 3: What is the average distance traveled?
<img src="Github Pages/Function 3/1.jpg" class="img-responsive" alt="">
<img src="Github Pages/Function 3/2.jpg" class="img-responsive" alt="" width="550">

### Function 4: How many riders include bike sharing regularly?
<img src="Github Pages/Function 4/1.jpg" class="img-responsive" alt="">
<img src="Github Pages/Function 4/2.jpg" class="img-responsive" alt="" width="600">

### Function 5: Analyze seasonal trends (e.g. PassType, Duration)
<img src="Github Pages/Function 5/1.jpg" class="img-responsive" alt="">
<img src="Github Pages/Function 5/2.jpg" class="img-responsive" alt="">

### Function 6: Bike transport to maintain bike levels
<img src="Github Pages/Function 6/1.jpg" class="img-responsive" alt="">
<img src="Github Pages/Function 6/2.jpg" class="img-responsive" alt="">
<img src="Github Pages/Function 6/3.jpg" class="img-responsive" alt="">

### Function 7: Breakdown of trip route category - passholder type combinations
<img src="Github Pages/Function 7/1.jpg" class="img-responsive" alt="">
<img src="Github Pages/Function 7/2.jpg" class="img-responsive" alt="" width="600">
