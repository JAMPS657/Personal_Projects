CREATE database olympics;

USE olympics;

CREATE table raw_data(ID int,
					BirthName char(25),
                    Sex char(1),
                    Age int,
                    Height_inches int,
					Weight_kg int,
                    Nation char(15),
					Region char(3),
                    Attending_year int,
                    Season char(10),
                    City char(20),
                    Sport char(25),
                    Medal char(10));

SELECT BirthName, Sex, Age, Height_inches, Weight_kg, Nation, Sport, Medal 
from raw_data;

SELECT Sex, Age, Attending_year
from raw_data;

SELECT Season, City, Sport
from raw_data;

