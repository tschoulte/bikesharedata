## Welcome to My Bikeshare Data Analyzer

Below is the documentation for my Python-coded bikeshare data analyzing script implemented for the [Capital One MindSumo Challenge](https://www.mindsumo.com/contests/bikeshare-data).

### Overview of Solution: App and Main Menu
Program consists of 3 files:
<img src="Github Pages/Main Menu/1.jpg" class="img-responsive" alt=""> </div>
1. Data.csv : This is the 35MB data file provided with the bikeshare data to be analyzed.
2. Main.py : This is my Python script file which will analyze the data.
3. Bike Share Data Analyzer.bat : This file, when ran, is responsible for running the Main.py file inside of a CMD prompt window. This allows for the program to be run independently of a compiler. As seen in later sceenshots, this greatly increases the ability to deploy this application without knowledge of how the code is working in the background.

After the Analyzer bat file is ran, the python script will deploy, revealing the main menu interface to my application.
<img src="Github Pages/Function 0/1.jpg" class="img-responsive" alt=""> </div>
There are 8 total options, ranging from 0 to 7.

Throughout my script, I have implemented protections against edge-case scenarios that would otherwise cause the program to crash and confuse the non-end user of this software. For example, trying to enter a number outside of 0 to 7 results in a message informing the user of this error. This input-guard functionality will be seen later in other aspects of the software.
<img src="Github Pages/Function 0/2.jpg" class="img-responsive" alt=""> </div>

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text
![useful image]({{ site.url }}/Github Pages/Function 0/1.jpg)
[Link](url) and ![Image](src)
<img src="/images/Function 0/1.jpg" alt="hi" class="inline"/>
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/tschoulte/bikesharedata/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
