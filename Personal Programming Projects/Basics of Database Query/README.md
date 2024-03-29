# Index
Home page [here](https://github.com/JAMPS657/Personal_Projects)

Code [here](https://github.com/JAMPS657/Personal_Projects/blob/main/Personal%20Programming%20Projects/Basics%20of%20Database%20Query/Database_Query.sql)

Project Selection [here](https://github.com/JAMPS657/Personal_Projects/tree/main/Personal%20Programming%20Projects)

# Summary
In this demonstration, I create, populate, and query a database. Specifically, I am using data from my [Exploration of Olympics Data](https://github.com/JAMPS657/Personal_Projects/tree/main/Personal%20Programming%20Projects/Analysis%20of%20Olympics%20Data) project. The script was created up using MySQL workbench, which has useful userinterface features such as importing or exporting data into and from the data base. This allows for other software programming languages (e.g. Python, R, etc.) to be used simultaneously with SQL code.

## Creating a Database
Using the "CREATE" statement, I create a database called "olympics".

![](Images/Creating_a_database.JPG)

## Creating A Table
Using the "CREATE" statement, I create a table within the "olympics" database and label it "raw_data". This allows us to populate the database (i.e. import data).

![](Images/Using_and_populating_database.JPG)

## Database Query
Now, with the relevant data uploaded; I use the "SELECT" statement to look at specific portions/columns of the data set. 

The first query is data relevant to the individual athlete. This would be important in identifying relevant stats to the athlete in question (e.g. Weight, Height, etc.). Note that there will be missing values for medals due to the fact that only 3 athletes/teams can plaCe in each event, with a few special cases.

![](Images/Exploring_database.JPG)

The second query is specific to Sex, Age, and year in attendance to the Olympics. This allows us to look at the relationship between timelines of Female and Male attendance to the olympics. My intuition being that there is a higher percentage of male participants before a particular year (e.g. women's rights revolution).

![](Images/Exploring_database2.JPG)

The third query is specific to Season, City, and Sport. This allows us to look at the relationship between what cities typically host the Winter or Summer Olympics. Additionally a relationship to what sports are hosted during which season.

![](Images/Exploring_database3.JPG)
