Project Selection [here](https://github.com/JAMPS657/Personal_Projects/tree/main/Personal%20Programming%20Projects)

# Analysis of COVID Immunization in Colorado
The project merges modules that were created to analyze their respective COVID data sets. 

# Project members

Andrew J. Otis and Sunwoo Park

## Datasets utilized

### 1. Primary dataset

CDC covid vax admin dataset by county:Overall US COVID-19 Vaccine
administration and vaccine equity data at county level. Data represents all
vaccine partners including jurisdictional partner clinics, retail pharmacies,
long-term care facilities, dialysis centers, Federal Emergency Management Agency
and Health Resources and Services Administration partner sites, and federal
entity facilities.

>Variables used: one dose/series completed/booster

>URL: [https://data.cdc.gov/Vaccinations/COVID-19-Vaccinations-in-the-United-States-County/8xkx-amqh](https://data.cdc.gov/Vaccinations/COVID-19-Vaccinations-in-the-United-States-County/8xkx-amqh)

### 2. Secondary supplement dataset

CDPHE socio-demographic dataset:This geography dataset includes
selected indicators  pertaining to population, income, education. This dataset is assembled annually from the U.S. Census American Community Survey American Factfinder website and is maintained by the Colorado Department of Public Health and Environment.

1. Income: These data contain selected census tract
level demographic indicators (estimates) from the 2015-2019 American Community Survey representing the percent of the population (for all persons) 

>Variables used: per capita income/median household income/mean household income

>URL: [https://data-cdphe.opendata.arcgis.com/datasets/CDPHE::income-poverty-census-tracts/about](https://data-cdphe.opendata.arcgis.com/datasets/CDPHE::income-poverty-census-tracts/about)

2. Education: These data contain selected census
tract level demographic indicators (estimates) from the 2015-2019 American
Community Survey representing the percent of the population (Age 25+) 

>Variables used: less than high school /high school diploma/non-bachelor's degree/bachelor's or higher

>URL: [https://data-cdphe.opendata.arcgis.com/datasets/CDPHE::educational-attainment-census-tracts/about](https://data-cdphe.opendata.arcgis.com/datasets/CDPHE::educational-attainment-census-tracts/about)

## Analysis question

To take COVID-19 data related to vaccination rates for the Colorado (state and county level), to propose possible relationships between vaccination trends vs demographic determinants.

> Is there a relation between vaccine completion rate and income level (capita/median)?

> Is there a relation between vaccine completion rate and education level attained (less than high school/high school diploma/non-bachelors degree/bachelors or higher)?

# Analysis results

1. CDC_vax.py (Primary dataset)

>Plot1: Vaccinated population by Date

>Plot2: Vaccinated population by County

2. CDPHE_demo.py (Secondary dataset)

>Plot1: Income by County

>Plot2: Education attainment by County

3. Vax_demo.py (combined overall analysis)

>Plot1: Vaccination complete rate & Income by County

>Plot2: Vaccination complete rate & Education attainment by County

# Description of program

1. CDC_vax.py (Primary dataset)

The dataset from CDC has daily reported county level records. We downloaded the filtered dataset that includes only Colorado counties due to large file size of
the full raw all states data. The script reads the source file into a dataframe using
Pandas and stores as a list for exporting to a csv file. Then, it aggregates the data by date summing county records to state level summary per day for time-series plot.

2. CDPHE_demo.py (Secondary dataset)

The datasets from CDPHE have Census tract level granularity, which is more detailed geographic information than county level. This script reads the two source files and merges together using 'FIPS' code as a join key. Then, it aggregates the records to county level summing population numbers in each county. Therefore, the percentage of target variables is recalculated dividing by total population of the county. Unnecessary Census tract codes are trimmed, but FIPS state and county codes remain after groupby process.

3. Vax_demo.py (combined overall analysis)

The program imports data from CDC vaccination and CDPHE demographic modules at the beginning, and joins into a single dataframe . It accepts user inputs of date chosen/sorting order/output file name/plotting to accommodate user's data need for analysis.

# How to run program

1. CDC_vax.py (Primary dataset)

>usage: python CDC_vax.py [-h] [-s (sort order)] [-x [(outfile)]] [-p]

No required argument. 'print' the records on screen is the default built-in command.

>'-s' or '--sort': sort the records by default

>>(sort order): default ('Date' and then 'FIPS'asc )

>'-x' or '--export': export the records to a file with comma delimiter.

>>(outfile): user defined

>'-p' or '--plot': create a chart on screen

2. CDPHE_demo.py (Secondary dataset)

>usage: python CDPHE_demo.py [-h] [-s (sort order)] [-x [(outfile)]] [-p]

No required argument. 'print' the records on screen is the default built-in command.

>'-s' or '--sort': sort the records by an user selected variable.

>>(sort order):

>>default ('FIPS'asc)

>>capita ('Per_Capita_Income ' desc)

>>median ('Median_Household_Income ' desc)

>>mean ('Mean_Household_Income ' desc)

>>lesshigh ('PCT_Education_Pop_AgeOver24_LessThan9th_Or_No_High_School_Dip' desc)

>>high ('PCT_Education_Pop_AgeOver24_High_School_Graduate' desc)

>>nonbach ('PCT_Education_Pop_AgeOver24_non-Bachelors' desc)

>>bachmore ('PCT_Education_Pop_AgeOver24_Bachelors_Higher' desc)

>'-x' or '--export': export the records to a file with comma delimiter.

>>(outfile): user defined

>'-p' or '--plot': create a chart on screen

3. Vax_demo.py (combined overall analysis)

>usage: python vax_demo.py [-h] [-s (sort order)] [-x [(outfile)]] [-p] (date)

>(date): user defined. required argument. The user can enter a date in 'yyyy -MM-dd' format to filter what date of the data to be used.

'print' the records on screen is the default built-in command.

>'-s' or '--sort': sort the records by an user selected variable.

>>(sort order): 

>>default ('FIPS' asc )
 
 >>1dose ('Administered_Dose1_Pop_Pct' desc)
 
 >>complete ('Series_Complete_Pop_Pct ' desc)
 
 >>booster ('Booster_Doses_Vax_Pct ' desc)
 
 >>capita ('Per_Capita_Income ' desc)
 
 >>median ('Median_Household_Income ' desc)
 
 >>mean ('Mean_Household_Income ' desc)
 
 >>lesshigh ('PCT_Education_Pop_AgeOver24_LessThan9th_Or_No_High_School_Dip'         desc)
 
 >>high ('PCT_Education_Pop_AgeOver24_High_School_Graduate' desc)
 
 >>nonbach ('PCT_Education_Pop_AgeOver24_non-Bachelors' desc)
 
 >>bachmore ('PCT_Education_Pop_AgeOver24_Bachelors_Higher' desc)

>'-x' or '--export': export the records to a file with comma delimiter.

>>(outfile): user defined

>'-p' or '--plot': create a chart on screen

4. unittest

>usage: python unittest_CDC.py
>usage: python unittest_CDPHE.py
