## Welcome to My Bikeshare Data Analyzer

Below is the documentation for my Python-coded bikeshare data analyzing script implemented for the [Capital One MindSumo Challenge](https://www.mindsumo.com/contests/bikeshare-data).

### Overview of Solution: App and Main Menu
The analysis program consists of the three following files:
<br>
<img src="Github Pages/Main Menu/1.jpg" class="img-responsive" alt="">
1. **Data.csv** : This is the 35MB data file provided with the bikeshare data to be analyzed.
2. **Main.py** : This is my Python script file which will analyze the data.
3. **Bike Share Data Analyzer.bat** : This file, when ran, is responsible for running the Main.py file inside of a CMD prompt window. This allows for the program to be run independently of a compiler. As seen in later sceenshots, this greatly increases the ability to deploy this application without knowledge of how the code is working in the background or the knowledge of a compiler.

After the Analyzer bat file is run, the python script will deploy, revealing the main menu interface to my application.
<img src="Github Pages/Function 0/1.jpg" class="img-responsive" alt="">
There are 8 options to select from, ranging from 0 to 7.

Throughout my script, I have implemented protections against edge-case scenarios that would otherwise cause the program to crash and confuse the non-end user of this software. For example, trying to enter a number outside of 0 to 7 results in a message informing the user of this error. This input-guard functionality will be seen later in other aspects of the software.
<img src="Github Pages/Function 0/2.jpg" class="img-responsive" alt="">
