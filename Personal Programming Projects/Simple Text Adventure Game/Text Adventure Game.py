
#---------------------------------------Initial Background-------------------------------------------------- #

# The concept(s) used in my final project is mainly Data Visualization of a large, pre-scraped dataset of the
# Olympic Games from 1896 - 2016. There is the reading in of files, but not with File I/O, instead the
# library pandas is utilized to read in the csv files.

# The goal of the final project is attempt to utilize Python to simply explore, clean, organize, and visualize
# a large data set (one I would typically use excel or Rstudio to analyze).

# The structure of the project/code is as follows, I will read in and merge two csv files that were provided
# during the submission of the final project, please save them to your directory. The code will read and merge
# the csv files. From that point, we will have our raw data set to work with and approach the available data
# through various perspectives in order to gain some sort of guided understanding.

# Lastly, I have included BOTH coding comments (for those who can view the code) as well as "viewer" comments
# displayed as the various analysis are run. This serves 2 purposes, the first is to make sense of the project
# from a coding perspective; but also to make the analysis logical for someone who is just seeing the results
# of the code being ran. Otherwise, it would appear that the program isn't doing anything at all.

# !Important Caveat!: To have code run as expected, the following must be done
#    "Ctrl+a" = to select everything THEN "Alt+shift+e" = to run code
#    The instructions listed above will allow ALL figures to be viewable simultaneously

#----------------------------------End of Initial Background-------------------------------------------------#

# Libraries we'll need to import inorder to perform the analysis/visualization
import numpy as np
# numpy is useful for performing up to high level mathematical operations on arrays

from matplotlib import pyplot as plt
# matplotlib is useful for data visualization and is a complimentary library to numpy, pyplot is an extension
# of matplotlib which aids in the processes previously mentioned.

import seaborn as sns
# seaborn is a complimentary library to matplotlib and will aid in visualizing the data

import pandas as pd
# pandas will be useful for reading in csv files, functioning in a similar manner to File I/O; but with the
# advantage of not having to explicitly open and close the file itself. Additionally, it is a complimentary
# library to numpy & matplotlib, optimizing code for array analysis.

# The function note_to_viewer() accepts an argument labeled 'reason'. Practically, it will aid in formatting
# strings(i.e. messages) on the display console.
def note_to_viewer(reason):
    print("\n" + reason)

note_to_viewer("Welcome! We'll be exploring data collected on the Olympics ranging from 1896-2016")

note_to_viewer("The following are the libraries we will be importing and working with in order to perform")
print("our analysis and visualizations.")
print("-numpy")
print("-pyplot from matplotlib")
print("-seaborn")
print("-pandas")

note_to_viewer("Let's read in the 1st csv file 'athlete_events.csv', this file contains information on")
print("individual athletes, such as weight, height, etc.")

    # Pre-Analysis 1
note_to_viewer("Pre-Analysis 1: Read in the First CSV")
data = pd.read_csv('athlete_events.csv')
print("Let's look at the first 10 data points of the original data set to check if the csv was read")
print(data.head(10))
note_to_viewer("Looks good!")

note_to_viewer("The table below provides some statistical info")
print("(e.g. mean and std. dev.,percentiles, etc.) of file we just read in.")
print(data.describe())

note_to_viewer("The table below shows what data types are contained in each column of the csv file.")
data.info()

note_to_viewer("Next, read in 2nd csv file 'datasets_31029_40943_noc_regions.csv'. This file contains")
print("information of the regions that have competed in the olympic games.")

    # Pre-Analysis 2
note_to_viewer("Pre-Analysis 2: Read in the Second CSV")
print("Now, let's do the same thing for our other csv")
regions = pd.read_csv('datasets_31029_40943_noc_regions.csv')

note_to_viewer("Let's take a look at the first 10 data points to check the csv was read")
print(regions.head(10))
note_to_viewer("Looks good!")

    # Pre-Analysis 3
note_to_viewer("Pre-Analysis 3: Merge The Two CSV Files")
print("Each file has been read in, but they are still separate, so we're going to merge the data sets.")

# The 'merged' data set is very important, because it is our combined data in its rawest/unaltered form
# of our data as arrays, where we can begin any kind of directed analysis/visualization
merged = pd.merge(data, regions, on='NOC', how='left')

note_to_viewer("Now let's check to see if the 2 files 'athlete_events.csv'&"
               "'datasets_31029_40943_noc_regions.csv' merged.")
merged.info()
note_to_viewer("Notice above, we have 2 more columns 'regions' & 'notes', confirming the merging of the files")

note_to_viewer("Let's get general sense of how big of a dataset we'll be working with.")
merged.count()
# Notes on Table
note_to_viewer("Each column of our merged data set contains thousands, up to tens-of-thousands elements.")
print("At this point, we are free to approach our data as we like to determine/visualize a number of things.")
print("However, depending on how we choose to approach the dataset, we may have to do some cleaning of the")
print("data (e.g. non-null values) before analysis/visualization.")


                             # ANALYSIS 1: A Look at Gold Medalists #
note_to_viewer("ANALYSIS 1: A Look at Gold Medalists")
# ANALYSIS 1-1
note_to_viewer("ANALYSIS 1-1: Filter for Only Gold Medalists")
print("We're going to create a data frame that contains ONLY athletes who've won a gold medal. Doesn't")
print("matter what sport or sex, any sport, and both Summer and Winter Olympic games")

goldMedals = merged[(merged.Medal == 'Gold')]
print(goldMedals.head(10))
note_to_viewer("The table above should ONLY containing athletes who have won a gold medal thus, we can move")
print("forward with our analysis")

# ANALYSIS 1-2
note_to_viewer("ANALYSIS 1-2 : Cleaning & Filtering the Merged Dataframe")
print("I think it it would interesting to take a deeper dive into the relationship")
print("between age and gold medals.")

# Code checks for non-number inputs (i.e. not an integer or decimal(floating number))
note_to_viewer("Notice that we do have non-null inputs (i.e. table shows 'True') in the 'Age' column")
print("of our merged dataset; we'll have to filter those non-null values out")
print(goldMedals.isnull().any())

# The code below removes the non-null values mentioned from our dataframe labeled 'goldMedals'
# (i.e. further modification of the dataframe).
goldMedals = goldMedals[np.isfinite(goldMedals['Age'])]
note_to_viewer("Now let's check to see if there are any more non-null values as part of our 'goldMedals' "
               "data frame")
print(goldMedals.isnull().any()) #'Age' column should show False, implying that we can do our visualizing
note_to_viewer("Looks good!")

# ANALYSIS 1-3
note_to_viewer("ANALYSIS 1-3: Distribution of Gold Medals in Relation to Age")
print("Now that we have a dataframe containing ONLY gold medalists AND workable values")

# We are plotting the 'Age' column of our 'goldMedals' data frame on the x-axis and number of gold medals
# won for the particular age values present.
note_to_viewer("Take a look at Figure 1")
def Distribution_of_gold_medalists():
    plt.tight_layout()
    plt.title('Distribution of Gold Medals')
    sns.countplot(x=goldMedals['Age'])
    plt.ylabel('# of Gold Medals')
    plt.show()

Distribution_of_gold_medalists()
# NOTES ON Figure 1 Stats
note_to_viewer("Let's look at the stats for our 'goldMedals' dataframe.")
print(goldMedals.describe())

note_to_viewer("Observing the Table above, we will ignore the columns 'ID' & 'Year'. As shown in Figure 1")
print("the mean age is about 26 years old with a std. dev. of about 6 years with a minimum age of 13")
print("and maximum of 64")

# NOTES ON Figure 1
note_to_viewer("Notes on Figure 1")
print("If you zoom in on the right tail of the distribution, you'll notice that people at the age")
print("of 60+ years old competed!")

note_to_viewer("These results have quite interested in exploring the gold winning 60 year olds, so")
print("that's where we'll direct the analysis.")

# ANALYSIS 1-4
note_to_viewer("ANALYSIS 1-4: From the the 'merged' dataframe, What Competitions Did These Older"
               " Athletes Compete In?")
# From the merged data set, we're filtering results greater than 60 from the 'Age' column and
# their associated sport from the 'Sport' column
sports_60up = merged['Sport'][merged['Age']>60]
print("Before graphing, let's make sure there are any non-null values present")
print(sports_60up.isnull().any())
note_to_viewer("Looks good!")

note_to_viewer("Take a look at Figure 2")
def sports_count_60up():
    plt.tight_layout()
    plt.figure(figsize=(10, 5))
    sns.countplot(x=sports_60up)
    plt.title('Distribution of Sports for Athletes 60+ Years Old')
    plt.ylabel('Total # of Competitors')
    plt.show()

sports_count_60up()
# NOTES ON Figure 2
note_to_viewer("Notes on Figure 2")
print("The figure shows see every event an athlete over the age of 60 has competed in as well as how many.")
print("Now I'm wondering which one of the sports listed these older athletes could have possibly won a gold")
print("medal in.")

# ANALYSIS 1-5
note_to_viewer("ANALYSIS 1-5: Have Any of these Athletes Above the Age of 60 Ever Won Gold, and in what"
               " Event?")
print("Since our 'goldMedal' dataframe has been cleaned to only contain gold medalists, we can now simply")
print("filter by the column 'Sport' and specify for those age 60yrs and up.")
gold_60up = goldMedals['Sport'][goldMedals['Age'] > 60]

note_to_viewer("Before graphing, let's make sure there are any non-null values present")
print(gold_60up.isnull().any())
note_to_viewer("Looks good!")

note_to_viewer("Take a look at Figure 3")
def G_medal_60up():
    plt.tight_layout()
    plt.figure(figsize=(10, 5))
    sns.countplot(x=gold_60up)
    plt.title('Distribution of Gold Medals for Athletes Over 60')
    plt.ylabel('# of Gold Medals')
    plt.show()

G_medal_60up()
# NOTES ON Figure 3
note_to_viewer("Notes on Figure 3")
print("Notice, a person above the age of 60 has won a gold medal in archery a total of 3 times")
print("while in Art Competitions, Roque, and Shooting; a person above the age of 60 has won gold once.")

note_to_viewer("Next, we'll exclude any gold medalist talk and determine what sports these older athletes")
print("would have participated in, not just the ones where they've won gold medals.")

note_to_viewer("Next, we'll take a look at gold medals with respect to the regions that have won them.")

                            # ANALYSIS 2: More Gold Medals, A Different Perspective #
note_to_viewer("ANALYSIS 2: More Gold Medals, A Different Perspective")
# ANALYSIS 2-1
note_to_viewer("ANALYSIS 2-1: Comparison of Gold Medals in Relation to Nation")
print("Let's take a quick glance at dataframe 'goldMedals' that we'll filter by region")
print("created in an earlier analysis.")

note_to_viewer("Below is a table representation of the data we will visualizing")
print(goldMedals.region.value_counts().reset_index(name='Medal').head(15))
# Same code from above, but labeling it 'totalG_Medals' for data manipulation
totalG_Medals = goldMedals.region.value_counts().reset_index(name='Medal').head(10)

print(totalG_Medals.isnull().any())
note_to_viewer("Looks good!")

note_to_viewer("Before graphing, let's make sure there are any non-null values present")
print(totalG_Medals.isnull().any())
note_to_viewer("Looks good!")

note_to_viewer("Take a look at Figure 4")
def Top_10G_medal_countries():
    g = sns.catplot(x="index", y="Medal", data=totalG_Medals,
                    height=6, kind="bar", palette="muted")
    g.despine(left=True)
    g.set_xlabels("Top 10 countries")
    g.set_ylabels("# of Gold Medals")
    plt.title('Top 10 Gold Medal Winning Countries')
    plt.show()

Top_10G_medal_countries()
# NOTES ON Figure 4
note_to_viewer("Notes on Figure 4")
print("Notice that USA has a significant lead with over 2500 gold medals won, with Russia and")
print("Germany coming in 2nd and 3rd respectively.")

note_to_viewer("I'm interested in the country that placed second(i.e. Russia) in the Top 10 gold")
print("winning countries. Additionally, what events Russia has won the most gold medals; so that's")
print("where we'll direct the analysis.")

#   ANALYSIS 2-2
note_to_viewer("ANALYSIS 2-2: What Events has Russia won the most gold medals in?")
goldMedalsRUS = goldMedals.loc[goldMedals['NOC'] == 'RUS'] # create the data frame

note_to_viewer("Take a look at the Table below")
print(goldMedalsRUS.Event.value_counts().reset_index(name='Gold Medals Won').head(20))
# NOTES ON TABLE
note_to_viewer("From the table above, can observe the first 20 events Russia has won gold medals in,")
print("ordered from the most to least.")

note_to_viewer("I'm now interested in the specific individuals of the sport with the most earned gold medals")
print("In this case, its synchronized swimming, women, so that's where we'll direct the analysis.")

#   ANALYSIS 2-3
# Determining specific individuals who have won gold is this even with 44 gold medals earned.
note_to_viewer("ANALYSIS 2-3: A Closer Look at Women's Synchronized Swimming")
syncswimGoldRUS = \
    goldMedalsRUS.loc[(goldMedalsRUS['Sport'] == 'Synchronized Swimming')\
    & (goldMedalsRUS['Sex'] == 'F')].sort_values(['Year'])

note_to_viewer("Take a look at the Table below")
print(syncswimGoldRUS.head(10))

# NOTES ON TABLE#
note_to_viewer("Notice that we have repeat names, meaning that some of these women had won gold medals in")
print("this particular event multiple times.")

note_to_viewer("This is the perfect transition to the final analysis of the program, female athletes in ")
print("the Olympics.")

                           # ANALYSIS 3: Female Olympian Attendance in the Olympics #
note_to_viewer("ANALYSIS 3: Female Olympian Attendance in the Olympics")
#   ANALYSIS 3-1
note_to_viewer("ANALYSIS 3-1: Graph a Line Plot of Women in the Winter Games Over Time")
# Code below creates our dataframe for the winter olympics and labeling it 'women_grouped_winter'
WomenOverTime = merged[(merged.Sex == 'F') & (merged.Season == 'Winter')]
print(WomenOverTime.head(20))
women_grouped_winter = WomenOverTime.groupby('Year')['Sex'].value_counts()
note_to_viewer("Above are the first 20 elements of our female-winter dataframe")

note_to_viewer("Below is a Table representation of the data visualized in Figure 5")
print(women_grouped_winter.describe)

note_to_viewer("Take a look at Figure 5")
def female_variation_winter():
    plt.figure(figsize=(10, 5))
    women_grouped_winter.loc[:,'F'].plot()
    plt.title('Winter Games: Variation of Female Athlete Attendance Over Time')
    plt.ylabel("# of Female Olympians")

female_variation_winter()

#   ANALYSIS 3-2
note_to_viewer("ANALYSIS 3-2: Graph a Line Plot of Women in the Summer Games Over Time")
# Code below creates our dataframe for the summer olympics and labeling it 'women_grouped_summer'
womenInOlympics = merged[(merged.Sex == 'F') & (merged.Season == 'Summer')]
print(womenInOlympics.head(20))
women_grouped_summer = womenInOlympics.groupby('Year')['Sex'].value_counts()
note_to_viewer("Above are the first 20 elements of our female-summer dataframe")

note_to_viewer("Below is a Table representation of the data visualized in Figure 6")
print(women_grouped_summer.describe)

note_to_viewer("Take a look at Figure 6")
def female_variation_summer():
    plt.figure(figsize=(10, 5))
    women_grouped_summer.loc[:,'F'].plot()
    plt.title('Summer Games: Variation of Female Athlete Attendance Over Time')
    plt.ylabel("# of Female Olympians")

female_variation_summer()

# NOTES ON figure 5 & 6
note_to_viewer("Comparison of Figures 5 & 6")
print("Overall, we can observe that a larger number of female Olympians are present during the summer games")
print("with a maximum attendance of over 6000 when compared to the winter games' maximum of slightly above")
print("2000.")

note_to_viewer("Additionally, we can observe that there is a similar and drastic spike in female attendance")
print("after the year 1980. Some of you history buffs might recall that it was during the 1980's where the")
print("'Women's Movement' was strong, and one of those instances where social barriers in at least American")
print("society; were looked at critically.")

note_to_viewer("Concluding Thoughts")
print("I find it super interesting that we were able to take an large volume data set and make some logical")
print("sense out of it. Thank you very much to both Ben and Afnan for their guidance during the course.")
print("This project has definitely provided perspective on how enlightening data can be, depending on how we")
print("look at it.")

note_to_viewer("Well, that's about it for the analysis. I hope you've learned something interesting about"
               " the Olympics")
print("To stop running the code and close all figures, simply hit the red square in the display console.")