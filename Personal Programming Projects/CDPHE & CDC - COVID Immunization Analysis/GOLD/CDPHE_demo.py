### CDPHE Composite Socio-Demographic Dataset (County)
### https://data.colorado.gov/Health/CDPHE-Composite-Socio-Demographic-Dataset-County-/rcsh-y5k8

### Income/Poverty (Census Tracts)
### https://data-cdphe.opendata.arcgis.com/datasets/CDPHE::income-poverty-census-tracts/about
### >Download>CSV>Download Options>Download file previously generated

### Educational Attainment (Census Tracts)
### https://data-cdphe.opendata.arcgis.com/datasets/CDPHE::educational-attainment-census-tracts/about
### >Download>CSV>Download Options>Download file previously generated


import pandas as pd
import argparse
import logging
import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt


## argparse section
parser = argparse.ArgumentParser(description='analyze socio-demographic data', conflict_handler='resolve')

## required argument (doesn't start with - 'dash'): reserved for combined module
parser.add_argument('dt',
                    metavar='<date>',
                    type=str,
                    help=argparse.SUPPRESS,    # not showing msg
                    nargs='?'
                    )

## optional arguments (starting with - 'dash')
# sort order
parser.add_argument('-s', '--sort',
                    metavar='<sort order>',
                    dest='srt',
                    choices=['default', '1dose', 'complete', 'booster', 'capita', 'median', 'mean', 'lesshigh', 'high', 'nonbach', 'bachmore']
                    )    # reserved for combined module: 1dose/complete/booster
# output a file
parser.add_argument('-x', '--export',
                    metavar='<outfile>',
                    dest='of',
                    nargs='?',
                    type=str
                    )
# output plots
parser.add_argument('-p', '--plot',
                    dest='plt',
                    action='store_true'
                    )
args = parser.parse_args()


## logging section
# log format
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s", "%Y-%m-%d %H:%M:%S")

# root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# file handler
fh = logging.FileHandler('CDPHE_demo.log', 'w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# stream handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
logger.addHandler(sh)


## class section
class CDPHE_data:
    def __init__(self):
        self.data = []
        self.load_data()

        if args.srt == 'capita':
            self.sort_by_capita()
        elif args.srt == 'median':
            self.sort_by_median()
        elif args.srt == 'mean':
            self.sort_by_mean()

        elif args.srt == 'lesshigh':
            self.sort_by_lesshigh()
        elif args.srt == 'high':
            self.sort_by_high()
        elif args.srt == 'nonbach':
            self.sort_by_nonbach()
        elif args.srt == 'bachmore':
            self.sort_by_bachmore()

        else:
            self.sort_by_default()

    def __iter__(self):
        return iter(self.data)

    def read_file(self):
        # read csv
        d_inc = pd.read_csv(f_inc)
        logging.debug(f'reading {f_inc}')
        d_edu = pd.read_csv(f_edu)
        logging.debug(f'reading {f_edu}')

        # join tables
        d_join = pd.merge(d_inc, d_edu, how='inner', on='FIPS')

        # set dataframe
        df2 = d_join

        # drop cols: unnecessary
        df2 = df2.filter(regex='^(?!Percent).+', axis=1)    # not start with 'Percent'
        df2 = df2.filter(regex='.+(?<!_y)$', axis=1)    # not ending with '_y': duplicated col
        df2 = df2.drop(columns=['OBJECTID_x', 'Tract_Name_x'])

        # add col: parse FIPS state (08: Colorado) + county (###) codes
        df2['FIPS_key'] = df2['FIPS'].map(str)
        df2['FIPS_key'] = '0' + df2['FIPS_key'].str[:4]

        # calculated col: non-bachelors (some college + associate degree)
        df2['Education_Population_AgeOver24_non-Bachelors'] = (df2['Education_Population_AgeOver24_HSD_Higher']
                                                               - df2['Education_Population_AgeOver24_High_School_Graduate']
                                                               - df2['Education_Population_AgeOver24_Bachelors_Higher']
                                                               )

        # rename cols: w/o suffix '_x'
        df2 = df2.rename(columns={'County_x': 'County'})
        df2 = df2.rename(columns={'Population_Total_x': 'Population_Total'})

        # rename cols
        df2 = df2.rename(columns={'Poverty_Per_Capita_Income': 'Per_Capita_Income'})
        df2 = df2.rename(columns={'Housing_Poverty_Median_Household_Income': 'Median_Household_Income'})
        df2 = df2.rename(columns={'Housing_Poverty_Mean_Household_Income': 'Mean_Household_Income'})

        # groupby FIPS_key
        df2 = df2.drop(columns=['FIPS'])    # drop census tracts
        df2_grp = df2.groupby(['FIPS_key']).sum().reset_index()

        # calculated cols: pct
        df2_grp['PCT_Education_Pop_AgeOver24_LessThan9th_Or_No_High_School_Dip'] = (
                    df2_grp['Education_Population_AgeOver24_LessThan9th_Or_No_High_School_Dip']
                    / df2_grp['Education_Population_AgeOver24'] * 100)
        df2_grp['PCT_Education_Pop_AgeOver24_High_School_Graduate'] = (
                    df2_grp['Education_Population_AgeOver24_High_School_Graduate']
                    / df2_grp['Education_Population_AgeOver24'] * 100)
        df2_grp['PCT_Education_Pop_AgeOver24_non-Bachelors'] = (df2_grp['Education_Population_AgeOver24_non-Bachelors']
                                                                / df2_grp['Education_Population_AgeOver24'] * 100)
        df2_grp['PCT_Education_Pop_AgeOver24_Bachelors_Higher'] = (
                    df2_grp['Education_Population_AgeOver24_Bachelors_Higher']
                    / df2_grp['Education_Population_AgeOver24'] * 100)

        # drop cols: unnecessary
        df2_grp = df2_grp.drop(columns=['Education_Population_AgeOver24_LessThan9th'])
        df2_grp = df2_grp.drop(columns=['Education_Population_AgeOver24_No_High_School_Diploma'])
        df2_grp = df2_grp.drop(columns=['Education_Population_AgeOver24_Some_College_NoDegree'])
        df2_grp = df2_grp.drop(columns=['Education_Population_AgeOver24_Associates_Degree'])
        df2_grp = df2_grp.drop(columns=['Education_Population_AgeOver24_Bachelors_Degree'])
        df2_grp = df2_grp.drop(columns=['Education_Population_AgeOver24_Graduate_Degree_Higher'])
        df2_grp = df2_grp.drop(columns=['Education_Population_AgeOver24_HSD_Higher'])

        # unique county name for join
        df2_cnty = df2[['FIPS_key', 'County']].copy().drop_duplicates()

        # append county name to aggregated table
        df2_grp = df2_grp.set_index('FIPS_key').join(df2_cnty.set_index('FIPS_key')).reset_index()

        # change cols order
        df2_grp = df2_grp[['FIPS_key',
                           'County',
                           'Population_Total',
                           'Per_Capita_Income',
                           'Median_Household_Income',
                           'Mean_Household_Income',
                           'Education_Population_AgeOver24',
                           'Education_Population_AgeOver24_LessThan9th_Or_No_High_School_Dip',
                           'Education_Population_AgeOver24_High_School_Graduate',
                           'Education_Population_AgeOver24_non-Bachelors',
                           'Education_Population_AgeOver24_Bachelors_Higher',
                           'PCT_Education_Pop_AgeOver24_LessThan9th_Or_No_High_School_Dip',
                           'PCT_Education_Pop_AgeOver24_High_School_Graduate',
                           'PCT_Education_Pop_AgeOver24_non-Bachelors',
                           'PCT_Education_Pop_AgeOver24_Bachelors_Higher'
                           ]]

        return df2_grp

    def agg_file(self):
        # write to aggregated file
        head = self.read_file().columns.values.tolist()
        lst = self.read_file().values.tolist()
        num_lin = 0

        with open(cf, 'w') as c:
            csv.writer(c, quoting=csv.QUOTE_ALL)
            c.write(str(head).strip('[').strip(']').replace("'", "").replace(" ", ""))
            c.write('\n')
            for r in lst:
                num_lin += 1
                line = f'{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]},{r[6]},{r[7]},{r[8]},{r[9]},{r[10]},{r[11]:.2f},{r[12]:.2f},{r[13]:.2f},{r[14]:.2f}\n'  # delimiter: comma
                c.write(line)
                logging.debug(f'line {num_lin} written to {cf}')

    def load_data(self):

        if not os.path.exists(f_inc):
            logging.critical(f'{f_inc} NOT exist')
            sys.exit(f"Go to following link and download CSV file\n{url_inc}")

        if not os.path.exists(f_edu):
            logging.critical(f'{f_edu} NOT exist')
            sys.exit(f"Go to following link and download CSV file\n{url_edu}")

        elif not os.path.exists(cf):
            logging.critical(f'{cf} NOT exist')
            self.read_file()
            self.agg_file()
            self.load_data()

        else:
            logging.debug(f'loading {cf}')
            num_lin = 0

            data = open(cf, 'r')
            data = csv.reader(data, delimiter=',', skipinitialspace=True)
            next(data)    # skip first row
            for r in data:
                num_lin += 1
                self.data.append((r[0],(r[1]),int(r[2]),int(r[3]),int(r[4]),int(r[5]),int(r[6]),int(r[7]),int(r[8]),int(r[9]),int(r[10]),float(r[11]),float(r[12]),float(r[13]),float(r[14])))
                logging.debug(f'line {num_lin} loaded to memory')

    def sort_by_default(self):  # sort by FIPS
        self.data.sort(key=lambda x: (x[0]))

    # def sort_by_county(self):  # sort by county name
    #     self.data.sort(key=lambda x: (x[1]))

    def sort_by_capita(self):  # sort by capita_income
        self.data.sort(key=lambda x: (x[3]), reverse=True)

    def sort_by_median(self):  # sort by median_income
        self.data.sort(key=lambda x: (x[4]), reverse=True)

    def sort_by_mean(self):  # sort by mean_income
        self.data.sort(key=lambda x: (x[5]), reverse=True)

    def sort_by_lesshigh(self):  # sort by less than high school
        self.data.sort(key=lambda x: (x[11]), reverse=True)

    def sort_by_high(self):  # sort by high school
        self.data.sort(key=lambda x: (x[12]), reverse=True)

    def sort_by_nonbach(self):  # sort by non-bachelors
        self.data.sort(key=lambda x: (x[13]), reverse=True)

    def sort_by_bachmore(self):  # sort by bachelors or higher
        self.data.sort(key=lambda x: (x[14]), reverse=True)

    def out_file(self):
        num_lin = 0

        # if args.of is None:    # output to sys.stdout
        #     for r in self.data:
        #         num_lin += 1
        #         line = f'{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]},{r[6]},{r[7]},{r[8]},{r[9]},{r[10]},{r[11]},{r[12]},{r[13]},{r[14]}\n'
        #         sys.stdout.write(line)
        #         logging.debug(f'line {num_lin} streamed out')

        if args.of is not None:    # output to a file
            with open(args.of, 'w') as of:
                csv.writer(of, quoting=csv.QUOTE_ALL)
                for r in self.data:
                    num_lin += 1
                    line = f'{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]},{r[6]},{r[7]},{r[8]},{r[9]},{r[10]},{r[11]},{r[12]},{r[13]},{r[14]}\n'
                    of.write(line)
                    logging.debug(f'line {num_lin} written to {args.of}')

    def out_plot(self):

        ## income: dot
        plt.plot([r[1] for r in self.data], [int(r[3]) for r in self.data], 'ro')    # per capita income
        plt.plot([r[1] for r in self.data], [int(r[4]) for r in self.data], 'go')    # median income
        plt.plot([r[1] for r in self.data], [int(r[5]) for r in self.data], 'bo')    # mean income

        plt.legend(['Per Capita Income', 'Median HH Income', 'Mean HH Income'], loc='upper right')
        plt.title('Income by County')
        plt.ylabel('Income')
        plt.xlabel('County')
        plt.xticks(rotation=90)
        plt.ticklabel_format(style='plain', axis='y')  # turn off sci notation
        plt.show()

        ## education: stacked bar
        labels = [r[1] for r in self.data]    # county name
        less_high = np.array([r[11] for r in self.data])
        high = np.array([r[12] for r in self.data])
        non_bach = np.array([r[13] for r in self.data])
        bach_more = np.array([r[14] for r in self.data])

        p1 = plt.bar(labels, less_high, label='Less than High School')
        p2 = plt.bar(labels, high, bottom=less_high, label='High School Diploma')
        p3 = plt.bar(labels, non_bach, bottom=less_high+high, label='non-Bachelors Degree')
        p4 = plt.bar(labels, bach_more, bottom=less_high+high+non_bach, label='Bachelors or higher')

        plt.legend()
        plt.title('Education Attainment by County')
        plt.ylabel('PCT of Education Attainment')
        plt.xlabel('County')
        plt.xticks(rotation=90)
        plt.show()


# global var: url links and file names
url_inc = 'https://data-cdphe.opendata.arcgis.com/datasets/CDPHE::income-poverty-census-tracts/about'
url_edu = 'https://data-cdphe.opendata.arcgis.com/datasets/CDPHE::educational-attainment-census-tracts/about'
f_inc = 'Income_Poverty_(Census_Tracts).csv'
f_edu = 'Educational_Attainment_(Census_Tracts).csv'
cf = 'CDPHE_demo.agg.csv'

def main():
    global url_inc, url_edu, f_inc, f_edu, cf

    logging.debug(f'executing {sys.argv[0]} (sort by {args.srt}) (output to {args.of}) (plot: {args.plt})')

    num_lin = 0
    for r in CDPHE_data():
        num_lin += 1
        print(str(r))
        logging.debug(f'line {num_lin} printed')

    if args.plt:
        CDPHE_data.out_plot(CDPHE_data())

    for arg in sys.argv[1:]:
        if arg == '-x' or arg == '--export':
            CDPHE_data.out_file(CDPHE_data())

    logging.debug(f'completed...{sys.argv[0]} (sort by {args.srt}) (output to {args.of}) (plot: {args.plt})')


if __name__ == '__main__':
    main()


### EOL