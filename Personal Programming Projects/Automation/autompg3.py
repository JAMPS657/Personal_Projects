import csv
import os.path
import sys
import requests  # to download the original file from the internet
import logging  # so that the program can create logs
import argparse  # to implement enhanced command-line parsing for the program
from operator import attrgetter  # to return a callable object that fetches attributes from its operand
import matplotlib.pyplot as plt
from collections import defaultdict  # utilizing a dictionary, rather than a named tuple to avoid challenges
                                     # related to immutability


def log_config():
    ''' The function creates loggs with respect to analysis of the data in a separate file and on the console
        respectively.
    '''
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("autompg2.log", 'w')
    fh.setLevel(logging.DEBUG)  # so the program creates a local log file, separate from the console
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)  # so the program creates a log message on the console
    logger.addHandler(sh)


class AutoMPG:
    ''' The class "AutoMPG" is representative of attributes associated with elements of the dataset
        "auto-mpg.data", referred to as "objects".
    '''

    def __init__(self, make, model, year, mpg):
        ''' The method initializes the attributes relevant to analysis from the relevant dataset.
                        -Attribute 1 is "make", string data type
                        -Attribute 2 is "model", string data type
                        -Attribute 3 is "year", integer data type
                        -Attribute 4 is "mpg", float data type
        '''
        self.make = str(make)  # first token in the “car name” field of the dataset

        self.model = str(model)  # all the other tokens in the “car name” field of the dataset
        # excluding the first token of a desired field

        self.year = 1900 + int(year)  # year of car model, a four-digit year that
        # corresponds to the field “model year” of the data set. Add 1900
        # to match actual year as shown in class OneNote

        self.mpg = float(mpg)  # miles per gallon, a floating point value that corresponds
        # to the “mpg” field of the data set

    def __repr__(self):
        ''' The method returns a string representation of the "attributes" previously initialized, with
            the added functionality of being to call the previous method "--str--(self)".
        '''
        return f"AutoMPG({self.make}, {self.model}, {self.year}, {self.mpg})"

    def __str__(self):
        ''' The method returns a string representation of the attributes previously initialized and will
            be shown in the order from left-to-right.
        '''
        return self.__repr__()

    def __eq__(self, other):
        ''' The method implements an equality comparison between two AutoMPG objects (itself and another).
            Utilizing all four attributes of AutoMPG and should only work between objects of the same type.
        '''
        if type(self) == type(other):
            logging.debug(f"...checking {self} equals {other}...")
            return (self.make, self.model, self.year, self.mpg) == (other.make, other.model, other.year, other.mpg)
        else:
            logging.error("ERROR: AutoMPG.equal Not Implemented")
            return NotImplemented

    def __lt__(self, other):
        ''' The method implements a less-than comparison between two AutoMPG objects (itself and another).
            Utilizing all four attributes of AutoMPG and should only work between objects of the same type.
        '''
        if type(self) == type(other):
            logging.debug(f"...checking {self} less than {other}...")
            return (self.make, self.model, self.year, self.mpg) < (other.make, other.model, other.year, other.mpg)
        else:
            logging.error("...ERROR: AutoMPG.less than Not Implemented...")
            return NotImplemented

    def __hash__(self):
        ''' The method calls the hash() function, which is a built-in function and returns the
            hash value (i.e. an integer which is used to quickly compare dictionary keys while
            looking at a dictionary.) of an object (provided it exists).
        '''
        return hash((self.make, self.model, self.year, self.mpg))


def parser_config():
    ''' The function serves the purpose of allowing for the user to enter arguments into the console.'''
    parser = argparse.ArgumentParser()  # benefits readability of code within the function

    # Arguments relevant to default sorting method part of the "AutoMPGData" class
    parser.add_argument("command", type=str, choices=['print', 'mpg_by_year', 'mpg_by_make', 'help'],
                        help="command to execute")
    # Arguments relevant to sorting methods that are part of the "AutoMPGData" class
    parser.add_argument("-s", "--sort", default="default", type=str, choices=['default', 'year', 'mpg'],
                        help="sorting order", dest="sort")
    # Additional arguments relevant to sorting average mpg woth respect to another field in the data
    parser.add_argument("-o", "--ofile", help="output file name", dest="output")
    # Supplementary argument that creates a plot of the additional argument "-o"
    parser.add_argument("-p", "--plot", help="produce graphical output", action="store_true")

    return parser.parse_args()


class AutoMPGData:
    ''' The class represents the entire AutoMPG data set, having a single attribute called "data"
        that is a list of AutoMPG objects. Upgraded with sorting methods.
    '''

    def __init__(self):
        ''' The method that will load the cleaned data file (auto-mpg.clean.txt) and
            instantiate AutoMPG objects and add them to the data attribute.
        '''
        self._load_data()

    def __iter__(self):
        '''  The method makes the class iterable. '''
        return iter(self.data)

    def __repr__(self):
        ''' The method is used to represent a class's objects as a string, avoiding ambiguity'''
        return "AutoMPGData()"

    def __str__(self):
        ''' The method  represents the class' objects as a string, making it readable'''
        return str(self.data)

    def _load_data(self):
        ''' The method will load the relevant cleaned data file and instantiate AutoMPG objects
            and add them to the "data" attribute. In the event that the file does not exist, then the
            method calls another method labeled "_clean_data(self)".
        '''
        if not os.path.exists("auto-mpg-data.txt"):
            logging.debug("...loading file...")
            self._get_data()

        if not os.path.exists("auto-mpg-clean.txt"):
            logging.debug("...cleaning file...")
            self._clean_data()

        self.data = []
        with open("auto-mpg-clean.txt", 'r') as f:
            reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
            for row in reader:
                rec = Record(row)
                car = AutoMPG(rec.name[0], rec.name[1], rec.year, rec.mpg)
                logging.debug(f"...creating object {car}...")
                self.data.append(car)

    def _clean_data(self):
        ''' The method will read the original data file line by line and use the expandtabs method
            available on str objects to convert the TAB character to spaces. The result is a cleaned
            version of the datset.
        '''
        with open("auto-mpg-data.txt", 'r') as r_file:
            with open("auto-mpg-clean.txt", 'w') as w_file:
                logging.debug("...cleaning file...")
                for row in r_file:
                    # Code for fixing erros present in data set, as stated by assignment description
                    row = row.replace('chevy', 'chevrolet')
                    row = row.replace('chevroelt', 'chevrolet')
                    row = row.replace('maxda', 'mazda')
                    row = row.replace('mercedes-benz', 'mercedes')
                    row = row.replace('toyouta', 'toyota')
                    row = row.replace('vokswagen', 'volkswagen')
                    row = row.replace('vw', 'volkswagen')

                    w_file.write(row.__str__().expandtabs(4))

    def sort_by_default(self):
        ''' The method that is used if the program is sorting AutoMPG objects by default (i.e. what was
            coded in the previous assignment).
        '''
        logging.info(" ...Sorting AutoMPG objects by default...")
        self.data.sort()

    def sort_by_year(self):
        ''' The method that is used if the program is sorting AutoMPG objects by year. '''
        logging.info(" ...Sorting AutoMPG objects by year...")
        self.data.sort(key=attrgetter('year', 'make', 'model', 'mpg'))

    def sort_by_mpg(self):
        ''' The method that is used if the program is sorting AutoMPG objects by mpg. '''
        logging.info(" ...Sorting AutoMPG objects by mpg...")
        self.data.sort(key=attrgetter('mpg', 'make', 'model', 'mpg'))

    def mpg_by_year(self):
        ''' The method that is used is determining average mpg by year. '''
        logging.info(" ...Determining average mpg by year and plotting...")
        year_count = defaultdict(int)
        year_mpg = defaultdict(float)

        for record in self.data:
            year_count[record.year] += 1
            year_mpg[record.year] += record.mpg

        for k, v in year_mpg.items():
            year_mpg[k] = round(v / year_count[k], 2)

        return year_mpg

    def mpg_by_make(self):
        ''' The method that is used is determining average mpg by model. '''
        logging.info(" ...Determining average mpg by model and plotting...")
        make_count = defaultdict(int)
        make_mpg = defaultdict(float)

        for record in self.data:
            make_count[record.make] += 1
            make_mpg[record.make] += record.mpg

        for k, v in make_mpg.items():
            make_mpg[k] = round(v / make_count[k], 2)

        return make_mpg

    def _get_data(self):
        ''' The method is called from the _load_data method, allowing for retreival of data from internet.
        '''
        logging.debug("...getting data from URL...")
        url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data'
        data_source = requests.get(url)
        logging.debug(f" ...response code {data_source.status_code} ...")
        with open("auto-mpg-data.txt", 'w') as f:
            f.write(data_source.text)


class Record:
    ''' The class passes the appropriate attributes into the AutoMPG class and Using tuple packing/unpacking,
        assign the list returned by the csv module for a row to create a Record object.
    '''

    def __init__(self, data_list):
        self.mpg = data_list[0]
        self.cyl = data_list[1]
        self.dis = data_list[2]
        self.hp = data_list[3]
        self.weight = data_list[4]
        self.accel = data_list[5]
        self.year = data_list[6]
        self.origin = data_list[7]

        # Clean the data by splitting the column containing make and model into their own respective
        # columns.
        self.name = data_list[8].split(maxsplit=1)

        # Conditions for when the event that only the brand is entered
        if len(self.name) < 2:
            self.name.append(" ")


def main():
    ''' In addition to added arguments (i.e. avg year by 'x'), the "main()" is where the graph creation
        is initiated.
    '''
    log_config()  # logs are initiated by the "main" function of the program
    args = parser_config()
    cars = AutoMPGData()

    if args.output:
        o_file = open(args.output, 'w')
    else:
        o_file = sys.stdout

    writer = csv.writer(o_file, quoting=csv.QUOTE_ALL)

    if args.command == 'print':
        logging.debug("...printing data...")

        # Conditions for sorting with respect to a single field of the data
        if args.sort == 'year':
            logging.debug("...sort by year...")
            cars.sort_by_year()
        elif args.sort == 'mpg':
            logging.debug("...sort by mpg to print...")
            cars.sort_by_mpg()
        else:
            logging.debug("...sort by default to print...")
            cars.sort_by_default()
        writer.writerow(['Make', 'Model', 'Year', 'MPG'])
        for car in cars:
            logging.debug(f" ...writing {car} to CSV...")
            writer.writerow([car.make, car.model, car.year, car.mpg])

    # Conditions for sorting with respect to a pair of fields in the data
    elif args.command == 'mpg_by_year':
        year_avg = cars.mpg_by_year()
        logging.debug("...avg mpg by year...")
        sorted_year_avg = dict(sorted(year_avg.items()))
        writer.writerow(['Year', 'Average MPG'])

        # Logic for creating the line plot
        for k, v in sorted_year_avg.items():
            writer.writerow([k, v])
        if args.plot:
            plt.plot(sorted_year_avg.keys(), sorted_year_avg.values())
            plt.savefig("avg_mpg_by_year_plot")

    elif args.command == 'mpg_by_make':
        make_avg = cars.mpg_by_make()
        logging.debug("...avg mpg by make...")
        sorted_make_avg = dict(sorted(make_avg.items()))
        writer.writerow(['Make', 'Average MPG'])

        # Logic for creating the line plot
        for k, v in sorted_make_avg.items():
            writer.writerow([k, v])
        if args.plot:
            plt.plot(sorted_make_avg.keys(), sorted_make_avg.values())
            plt.xticks(rotation=75)
            plt.savefig("avg_mpg_by_make_plot")

    o_file.close()


if __name__ == '__main__':
    main()