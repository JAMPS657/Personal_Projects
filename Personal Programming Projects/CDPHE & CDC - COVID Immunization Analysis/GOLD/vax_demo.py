### Combining module for CDC vax and CDPHE demo data


import argparse
## argparse section
parser = argparse.ArgumentParser(description='analyze COVID vaccination and socio-demographic data')

## required argument (doesn't start with - 'dash')
parser.add_argument('dt',
                    metavar='<date>',
                    type=str,
                    help="enter date in 'yyyy-MM-dd' format (from 2021-08-03 to 2022-05-10)"
                    )

## optional arguments (starting with - 'dash')
# sort order
parser.add_argument('-s', '--sort',
                    metavar='<sort order>',
                    dest='srt',
                    choices=['default', '1dose', 'complete', 'booster', 'capita', 'median', 'mean', 'lesshigh', 'high', 'nonbach', 'bachmore']
                    )
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


from CDC_vax import *
from CDPHE_demo import *


## logging section
# log format
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s", "%Y-%m-%d %H:%M:%S")

# root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# file handler
fh = logging.FileHandler('vax_demo.log', 'w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# stream handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
logger.addHandler(sh)


class vax_demo:
    def __init__(self):
        self.data = []
        self.load_df()

        if args.srt == '1dose':
            self.sort_by_1dose()
        elif args.srt == 'complete':
            self.sort_by_cmplt()
        elif args.srt == 'booster':
            self.sort_by_boost()

        elif args.srt == 'capita':
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

    def join_data(self):
        df1 = CDC_data.read_file(CDC_data())
        df2 = CDPHE_data.read_file(CDPHE_data())
        logging.debug(f'joining vax and demo dataframes')

        # replace value: trim ' County' in 'County' col
        df1['County'] = df1['County'].replace(regex=r'( County)$', value='')

        # drop dup col for join
        df2 = df2.drop(columns=['County'])

        # join tables
        df = df1[df1['Date'] == date_chosen].set_index('FIPS').join(df2.set_index('FIPS_key')).reset_index()

        # convert datetime to date
        df['Date'] = pd.to_datetime(df['Date']).dt.date

        # drop cols: unnecessary
        df = df.drop(columns=['Completeness_pct'])

        return df

    def join_file(self):
        # write to joined file
        head = self.join_data().columns.values.tolist()
        lst = self.join_data().values.tolist()
        num_lin = 0

        with open(jf, 'w') as c:
            csv.writer(c, quoting=csv.QUOTE_ALL)
            c.write(str(head).strip('[').strip(']').replace("'", "").replace(" ", ""))
            c.write('\n')
            for r in lst:
                num_lin += 1
                line = f'{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]},{r[6]},{r[7]},{r[8]},{r[9]},{r[10]},{r[11]},{r[12]},{r[13]},{r[14]},{r[15]},{r[16]},{r[17]},{r[18]},{r[19]},{r[20]:.2f},{r[21]:.2f},{r[22]:.2f},{r[23]:.2f}\n'  # delimiter: comma
                c.write(line)
                logging.debug(f'line {num_lin} written to {jf}')

    def load_df(self):

        self.join_data()
        self.join_file()

        logging.debug(f'loading {jf}')
        num_lin = 0

        data = open(jf, 'r')
        data = csv.reader(data, delimiter=',', skipinitialspace=True)
        next(data)  # skip first row
        for r in data:
            num_lin += 1
            self.data.append((r[0], r[1], r[2], r[3],
                              float(r[4]), float(r[5]), float(r[6]), float(r[7]), float(r[8]), float(r[9]), float(r[10]),
                              int(r[11]), int(r[12]), int(r[13]), int(r[14]),
                              int(r[15]), int(r[16]), int(r[17]), int(r[18]), int(r[19]),
                              float(r[20]), float(r[21]), float(r[22]), float(r[23])))
            logging.debug(f'line {num_lin} loaded to memory')

    def sort_by_default(self):  # sort by FIPS
        self.data.sort(key=lambda x: (x[0]))

    def sort_by_1dose(self):  # sort by Administered_Dose1_Pop_Pct desc
        self.data.sort(key=lambda x: (x[5]), reverse=True)

    def sort_by_cmplt(self):  # sort by Series_Complete_Pop_Pct desc
        self.data.sort(key=lambda x: (x[7]), reverse=True)

    def sort_by_boost(self):  # sort by Booster_Doses_Vax_Pct desc
        self.data.sort(key=lambda x: (x[9]), reverse=True)

    def sort_by_capita(self):  # sort by capita_income
        self.data.sort(key=lambda x: (x[12]), reverse=True)

    def sort_by_median(self):  # sort by median_income
        self.data.sort(key=lambda x: (x[13]), reverse=True)

    def sort_by_mean(self):  # sort by mean_income
        self.data.sort(key=lambda x: (x[14]), reverse=True)

    def sort_by_lesshigh(self):  # sort by PCT_less than high school desc
        self.data.sort(key=lambda x: (x[20]), reverse=True)

    def sort_by_high(self):  # sort by PCT_high school desc
        self.data.sort(key=lambda x: (x[21]), reverse=True)

    def sort_by_nonbach(self):  # sort by PCT_non-bachelors desc
        self.data.sort(key=lambda x: (x[22]), reverse=True)

    def sort_by_bachmore(self):  # sort by PCT_bachelors or higher desc
        self.data.sort(key=lambda x: (x[23]), reverse=True)

    def out_file(self):
        num_lin = 0

        # if args.of is None:    # output to sys.stdout
        #     for r in self.data:
        #         num_lin += 1
        #         line = f'{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]},{r[6]},{r[7]},{r[8]},{r[9]},{r[10]},{r[11]},{r[12]},{r[13]},{r[14]},{r[15]},{r[16]},{r[17]},{r[18]},{r[19]},{r[20]},{r[21]},{r[22]},{r[23]}\n'
        #         sys.stdout.write(line)
        #         logging.debug(f'line {num_lin} streamed out')

        if args.of is not None:    # output to a file
            with open(args.of, 'w') as of:
                csv.writer(of, quoting=csv.QUOTE_ALL)
                for r in self.data:
                    num_lin += 1
                    line = f'{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]},{r[6]},{r[7]},{r[8]},{r[9]},{r[10]},{r[11]},{r[12]},{r[13]},{r[14]},{r[15]},{r[16]},{r[17]},{r[18]},{r[19]},{r[20]},{r[21]},{r[22]},{r[23]}\n'
                    of.write(line)
                    logging.debug(f'line {num_lin} written to {args.of}')

    def out_plot(self):

        ## income: dot    # r[7]: 'Series_Complete_Pop_Pct'
        plt.plot([r[12] for r in self.data], [r[7] for r in self.data], 'bo')  # r[12]: per capita income
        plt.plot([r[13] for r in self.data], [r[7] for r in self.data], 'go')  # r[13]: median income

        plt.legend(['Per Capita Income', 'Median HH Income'], loc='lower right')
        plt.title('PCT of Vax Completed Pop by Income by County')
        plt.ylabel('PCT of Vax Completed Pop')
        plt.ylim(0, 100)
        plt.xlabel('Income')
        plt.xticks(rotation=90)
        plt.ticklabel_format(style='plain', axis='x')  # turn off sci notation
        plt.show()

        ## education: stacked bar (hybrid)
        labels = [r[2] for r in self.data]  # r[2]: county name
        less_high = np.array([r[20] for r in self.data])
        high = np.array([r[21] for r in self.data])
        non_bach = np.array([r[22] for r in self.data])
        bach_more = np.array([r[23] for r in self.data])

        plt.plot([r[2] for r in self.data], [r[7] for r in self.data], 'bo')  # r[7]: 'Series_Complete_Pop_Pct'
        p1 = plt.bar(labels, less_high)
        p2 = plt.bar(labels, high, bottom=less_high)
        p3 = plt.bar(labels, non_bach, bottom=less_high + high)
        p4 = plt.bar(labels, bach_more, bottom=less_high + high + non_bach)

        plt.legend(['Vax Complete Pop Pct', 'Less than High School', 'High School Diploma', 'non-Bachelors Degree',
                    'Bachelors or higher'], loc='upper right')
        plt.title('PCT of Vax Completed Pop & Edu Attainment by County')
        plt.ylabel('Percentage')
        plt.xlabel('County')
        plt.xticks(rotation=90)
        plt.show()


# global var
date_chosen = str(args.dt)
jf = 'vax+demo.join.csv'

def main():
    global date_chosen, jf

    logging.debug(f'executing {sys.argv[0]} {args.dt} (sort by {args.srt}) (output to {args.of}) (plot: {args.plt})')

    num_lin = 0
    for r in vax_demo():
        num_lin += 1
        print(str(r))
        logging.debug(f'line {num_lin} printed')

    if args.plt:
        vax_demo.out_plot(vax_demo())

    for arg in sys.argv[1:]:
        if arg == '-x' or arg == '--export':
            vax_demo.out_file(vax_demo())

    logging.debug(f'completed...{sys.argv[0]} {args.dt} (sort by {args.srt}) (output to {args.of}) (plot: {args.plt})')


if __name__ == '__main__':
    main()


### EOL