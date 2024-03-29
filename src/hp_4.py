# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    return [datetime.strptime(dt, "%Y-%m-%d").strftime('%d %b %Y') for dt in old_dates]


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        
        raise TypeError()
    a = []
    dt = datetime.strptime(start, '%Y-%m-%d')
    for i in range(n):
        a.append(dt + timedelta(days=i))
    return a

def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    x = date_range(start_date, len(values))
    return list(zip(x, values))


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    header = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".split(','))
    fee_report_dict = defaultdict(float)
    with open(infile, 'r') as fl:
        ln = DictReader(fl, fieldnames=header)
        rows = [row for row in ln]
    rows.pop(0)
    
    for row in rows:
        patronID = row['patron_id']
        date_due = datetime.strptime(row['date_due'], "%m/%d/%Y")
        date_returned_on = datetime.strptime(row['date_returned'], "%m/%d/%Y")
        days_in_late = (date_returned_on - date_due).days
        fee_report_dict[patronID]+= 0.25 * days_in_late if days_in_late > 0 else 0.0
        
    outputs = [
        {'patron_id': payn, 'late_fees': f'{fsrt:0.2f}'} for payn, fsrt in fee_report_dict.items()
    ]
    with open(outfile, 'w') as fee_id:
        fee_id_output = DictWriter(fee_id,['patron_id', 'late_fees'])
        fee_id_output.writeheader()
        fee_id_output.writerows(outputs)



# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
