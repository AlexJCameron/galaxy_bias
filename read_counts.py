import numpy as np
import pandas as pd

def rm_empty(q_list):
    """Removes empty entries from a list.

    Parameters
    ----------
    q_list : list
        The list to be cleaned.

    """
    new_list = []
    for item in q_list:
        if not len(item) == 0:
            new_list.append(item)
    return new_list

def get_counts_data(count_filename, delim=' '):
    """Takes the filename of a flat file containing the data and returns it as a pandas DataFrame

    Parameters
    ----------
    count_filename : str
        Filename of data
    delim : str
        Data separator

    Returns
    -------
    count_data : pandas DataFrame
        The count data for the dataset

    """
    count_file = open(count_filename)
    count_lines = rm_empty(count_file.read().split('\n'))
    count_file.close()
    header = rm_empty(count_lines[0].split(delim))
    count_lines = count_lines[1:]
    count_data = pd.DataFrame(columns=header)
    for line in count_lines:
        line_data = rm_empty(line.split(delim))
        vals = []
        for val in line_data[1:]:
            vals.append(float(val))
        count_data.loc[line_data[0]] = vals

    return count_data

def read_multi_type(counts_filename):
    """Assumed structure:
    FIELD+NAME (area) (ET) (scET) (LT) (scLT)
    """
    count_file = open(counts_filename)
    count_lines = rm_empty(count_file.read().split('\n')[1:])
    count_file.close()

    early_counts = []
    late_counts = []

    for line in count_lines:
        split_line = line.split(' ')
        scET = float(split_line[3])
        scLT = float(split_line[5])
        early_counts.append(scET)
        late_counts.append(scLT)

    return early_counts, late_counts


def counts_meanvar(count_data, count_type='WhtCount'):
    """Returns the mean and variance of field counts from a pandas DataFrame

    Parameters
    ----------
    count_data : pandas DataFrame
        The field counts data in a DataFrame
    count_type : str
        The count column to use

    Returns
    -------
    mean, var : float
        The mean and variance of the sample of counts

    """
    mean = np.mean(count_data[count_type])
    var = np.var(count_data[count_type])
    return mean, var

if __name__=='__main__':
    from sys import argv
    script, count_file = argv
    cdat = get_counts_data(count_file)
    print counts_meanvar(cdat)
