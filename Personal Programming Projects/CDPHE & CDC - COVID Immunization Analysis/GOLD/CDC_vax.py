### COVID-19 Vaccinations in the United States, County
### https://data.cdc.gov/Vaccinations/COVID-19-Vaccinations-in-the-United-States-County/8xkx-amqh
### >View Data>Filter>Add a New Filter Condition>Recip_State>CO>Export>Download>CSV


import pandas as pd
import argparse
import logging
import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt

## argparse section
parser = argparse.ArgumentParser(description='analyze COVID vaccination data', conflict_handler='resolve')

## required argument (doesn't start with - 'dash'): reserved for combined module
parser.add_argument('dt',
                    metavar='<date>',
                    type=str,
                    help=argparse.SUPPRESS,  # not showing msg
                    nargs='?'
                    )

## optional arguments (starting with - 'dash')
# sort order
parser.add_argument('-s', '--sort',
                    metavar='<sort order>',
                    dest='srt',
                    choices=['default', '1dose', 'complete', 'booster', 'capita', 'median', 'mean', 'lesshigh', 'high',
                             'nonbach', 'bachmore']
                    )  # reserved for combined module: 'capita', 'median', 'mean', 'lesshigh', 'high', 'nonbach', 'bachmore'
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
fh = logging.FileHandler('CDC_vax.log', 'w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# stream handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
logger.addHandler(sh)


class CDC_data:
    def __init__(self):
        self.data = []
        self.data_agg = []
        self.load_data()
        self.sort_by_default()

    def __iter__(self):
        return iter(self.data)

    def read_file(self):
        # read csv
        d_cov = pd.read_csv(f_cov)
        logging.debug(f'reading {f_cov}')

        # set dataframe
        df1 = d_cov

        # drop cols: unnecessary
        df1 = df1.filter(regex='.+(?<!Plus)$', axis=1)  # not ending with 'Plus'
        df1 = df1.filter(regex='.+(?<!PlusPop_Pct)$', axis=1)  # not ending with 'PlusPop_Pct'
        df1 = df1.filter(regex='.+(?<!Plus_Vax_Pct)$', axis=1)  # not ending with 'Plus_Vax_Pct'
        df1 = df1.filter(regex='^(?!SVI_).+', axis=1)  # not start with 'SVI_'
        df1 = df1.filter(regex='.+(?<!_SVI)$', axis=1)  # not ending with '_SVI'
        df1 = df1.filter(regex='.+(?<!_Equity)$', axis=1)  # not ending with '_Equity'
        df1 = df1.filter(regex='.+(?<!PlusPop)$', axis=1)  # not ending with 'PlusPop'
        df1 = df1.drop(columns=['MMWR_week', 'Metro_status', 'Series_Complete_5to17', 'Series_Complete_5to17Pop_Pct',
                                'Census2019_5to17Pop'])

        # filter rows: only Colorado, not unknown FIPS
        df1 = df1[df1['Recip_State'] == 'CO']
        df1 = df1[df1['FIPS'] != 'UNK']

        # replace value: trim ' County' in 'Recip_County' col
        df1['Recip_County'] = df1['Recip_County'].replace(regex=r'( County)$', value='')

        # rename cols: w/o prefix 'Recip_'
        df1 = df1.rename(columns={'Recip_County': 'County'})
        df1 = df1.rename(columns={'Recip_State': 'State'})

        # convert str to date format
        df1['Date'] = pd.to_datetime(df1['Date'], format='%m/%d/%Y')

        # filter rows: after 2021-08-02 for data consistency
        df1 = df1[df1['Date'] > '2021-08-02']

        return df1

    def clean_file(self):
        # write to clean file
        head = self.read_file().columns.values.tolist()
        lst = self.read_file().values.tolist()
        num_lin = 0

        with open(cf, 'w') as c:
            csv.writer(c, quoting=csv.QUOTE_ALL)
            c.write(str(head).strip('[').strip(']').replace("'", "").replace(" ", ""))
            c.write('\n')
            for r in lst:
                num_lin += 1
                line = f'{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]},{r[6]},{r[7]},{r[8]},{r[9]},{r[10]},{r[11]}\n'  # delimiter: comma
                c.write(line)
                logging.debug(f'line {num_lin} written to {cf}')

    def agg_data(self):
        # groupby date
        df1_grp = self.read_file().drop(columns=['FIPS', 'County'])  # drop county
        df1_grp = df1_grp.groupby(['Date']).sum().reset_index()

        # calculated cols: pct
        df1_grp['Administered_Dose1_Pop_Pct'] = (df1_grp['Administered_Dose1_Recip'] / df1_grp['Census2019'] * 100)
        df1_grp['Series_Complete_Pop_Pct'] = (df1_grp['Series_Complete_Yes'] / df1_grp['Census2019'] * 100)
        df1_grp['Booster_Doses_Vax_Pct'] = (
                    df1_grp['Booster_Doses'] / df1_grp['Series_Complete_Yes'] * 100)  # not out of tot pop

        # drop col
        df1_grp = df1_grp.drop(columns=['Completeness_pct'])

        return df1_grp

    def agg_file(self):
        # write to agg file
        head = self.agg_data().columns.values.tolist()
        lst = self.agg_data().values.tolist()
        num_lin = 0

        with open(af, 'w') as c:
            csv.writer(c, quoting=csv.QUOTE_ALL)
            c.write(str(head).strip('[').strip(']').replace("'", "").replace(" ", ""))
            c.write('\n')
            for r in lst:
                num_lin += 1
                line = f'{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]},{r[6]},{r[7]}\n'  # delimiter: comma
                c.write(line)
                logging.debug(f'line {num_lin} written to {af}')

    def load_data(self):

        if not os.path.exists(f_cov):
            logging.critical(f'{f_cov} NOT exist')
            sys.exit(f"Go to following link and download CSV file\n{url_cov}")

        if not os.path.exists(cf):
            logging.critical(f'{cf} NOT exist')
            self.read_file()
            self.clean_file()
            self.load_data()

        if not os.path.exists(af):
            logging.critical(f'{af} NOT exist')
            self.agg_data()
            self.agg_file()
            self.load_data()

        else:
            # part.1: clean
            logging.debug(f'loading {cf}')
            num_lin = 0

            data = open(cf, 'r')
            data = csv.reader(data, delimiter=',', skipinitialspace=True)
            next(data)  # skip first row
            for r in data:
                num_lin += 1
                self.data.append((r[0], r[1], r[2], r[3], float(r[4]), float(r[5]), float(r[6]), float(r[7]),
                                  float(r[8]), float(r[9]), float(r[10]), float(r[11])))
                logging.debug(f'line {num_lin} loaded to memory [data]')

            # part.2: agg by date
            logging.debug(f'loading {af}')
            num_lin = 0

            data_agg = open(af, 'r')
            data_agg = csv.reader(data_agg, delimiter=',', skipinitialspace=True)
            next(data_agg)  # skip first row
            for r in data_agg:
                num_lin += 1
                self.data_agg.append(
                    (r[0], float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5]), float(r[6]), float(r[7])))
                logging.debug(f'line {num_lin} loaded to memory [data_agg]')

    def sort_by_default(self):  # sort by date x[0], FIPS x[1]
        self.data.sort(key=lambda x: (x[0], x[1]))

    def out_file(self):
        num_lin = 0

        # if args.of is None:    # output to sys.stdout
        #     for r in self.data:
        #         num_lin += 1
        #         line = f'{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]},{r[6]},{r[7]},{r[8]},{r[9]},{r[10]},{r[11]}\n'
        #         sys.stdout.write(line)
        #         logging.debug(f'line {num_lin} streamed out')

        if args.of is not None:  # output to a file
            with open(args.of, 'w') as of:
                csv.writer(of, quoting=csv.QUOTE_ALL)
                for r in self.data:
                    num_lin += 1
                    line = f'{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]},{r[6]},{r[7]},{r[8]},{r[9]},{r[10]},{r[11]}\n'
                    of.write(line)
                    logging.debug(f'line {num_lin} written to {args.of}')

    def out_plot(self):

        ## time-series
        x = [r[0].replace(' 00:00:00', '') for r in self.data_agg]
        plt.plot(x, [float(r[1]) for r in self.data_agg], 'b.')  # r[1]: 1dose
        plt.plot(x, [float(r[3]) for r in self.data_agg], 'y.')  # r[3]: series completed
        plt.plot(x, [float(r[5]) for r in self.data_agg], 'g.')  # r[5]: booster

        plt.legend(['1 dose', 'Series Completed', 'Booster'], loc='lower right')
        plt.title('Vaccinated Population in CO by Date')
        plt.ylabel('Population')
        plt.xlabel('Date')
        plt.xticks(rotation=90)
        plt.ticklabel_format(style='plain', axis='y')  # turn off sci notation
        plt.show()

        ## bar by county
        max_dt = self.agg_data()['Date'].max()  # most recent date
        filt_data = [r for r in self.data if r[0] == str(max_dt)]
        filt_data.sort(key=lambda x: (x[5]), reverse=True)  # x[5]: 1dose pop

        labels = [r[2] for r in filt_data]  # r[2]: county name
        onedose = np.array([r[5] for r in filt_data])
        cmplt = np.array([r[7] for r in filt_data])
        boost = np.array([r[9] for r in filt_data])

        p1 = plt.bar(labels, onedose, width=0.9)
        p2 = plt.bar(labels, cmplt, width=0.5)
        p3 = plt.bar(labels, boost, width=0.3)

        plt.legend(['1 dose', 'Series Completed', 'Booster'], loc='upper right')
        max_dt_tr = str(max_dt).replace(' 00:00:00', '')
        plt.title(f'Vaccinated Population by County ({max_dt_tr})')
        plt.ylabel('Population')
        plt.xlabel('County')
        plt.xticks(rotation=90)
        plt.show()


# global var: url links and file names
url_cov = 'https://data.cdc.gov/Vaccinations/COVID-19-Vaccinations-in-the-United-States-County/8xkx-amqh'
f_cov = 'COVID-19_Vaccinations_in_the_United_States_County.csv'
cf = 'CDC_vax.clean.csv'
af = 'CDC_vax.agg.csv'

def main():
    global url_cov, f_cov, cf, af

    logging.debug(f'executing {sys.argv[0]} (sort by {args.srt}) (output to {args.of}) (plot: {args.plt})')

    num_lin = 0
    for r in CDC_data():
        num_lin += 1
        print(str(r))
        logging.debug(f'line {num_lin} printed')

    if args.plt:
        CDC_data.out_plot(CDC_data())

    for arg in sys.argv[1:]:
        if arg == '-x' or arg == '--export':
            CDC_data.out_file(CDC_data())

    logging.debug(f'completed...{sys.argv[0]} (sort by {args.srt}) (output to {args.of}) (plot: {args.plt})')


if __name__ == '__main__':
    main()

### EOL