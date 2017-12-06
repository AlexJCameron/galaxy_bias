import matplotlib
matplotlib.rcParams.update({'font.size': 14})

from matplotlib import rc
rc('font',**{'family':'serif','serif':[]})
rc('text', usetex=True)

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import read_counts

def pick_new_sample(data_list):
    """From a list of data will pick a new sample of the same length with repetition

    Parameters
    ----------
    data_list : list
        A list of the data_points

    Returns
    -------
    new_set : list
        A randomly selected (with repetition) set from the original data

    """
    num_points = len(data_list)
    new_set = []
    for n in range(num_points):
        rand_ind = np.random.randint(num_points)
        new_set.append(data_list[rand_ind])
    return new_set

def get_meanvar(dataset):
    """Returns mean and variance of list of values
    """
    mean = np.mean(dataset)
    var = np.var(dataset)
    return mean, var

def compute_bias(mean_N, var_N, sigDM2=0.012244):
    """Computes the galaxy bias from mean and variance of galaxy counts and sigma(DarkMatter)^2
    (see Roberston 2010)
    """
    return ((var_N - mean_N)/(mean_N**2*sigDM2))**0.5

def MC_bootstrap(counts_filename, no_repetitions, sigDM2=0.012244, count_type='WhtCount'):
    """Conducts a Monte-Carlo Bootstrapping error analysis on a set of counts.

    Will randomly select from the set of counts a number of times, calculate the bias for that set.plot

    Parameters
    ----------
    counts_filename : str
        Filename of the count_data file
    no_repetitions : int
        Number of biases to calculate

    Returns
    -------
    bias_set : list
        List of biases calculated in the analysis

    """
    count_data = read_counts.get_counts_data(counts_filename)
    count_list = list(count_data[count_type])
    bias_set = []
    for rep in range(no_repetitions):
        new_counts = pick_new_sample(count_list)
        mean_N, var_N = get_meanvar(new_counts)
        if var_N >= mean_N:
            new_bias = compute_bias(mean_N, var_N, sigDM2=sigDM2)
        else:
            new_bias = 0
        bias_set.append(new_bias)
    return bias_set

def MC_bootstrap_list(count_list, no_repetitions, sigDM2=0.012244):
    """Conducts a Monte-Carlo Bootstrapping error analysis on a set of counts.

    Will randomly select from the set of counts a number of times, calculate the bias for that set.plot

    Parameters
    ----------
    counts_filename : str
        Filename of the count_data file
    no_repetitions : int
        Number of biases to calculate

    Returns
    -------
    bias_set : list
        List of biases calculated in the analysis

    """
    bias_set = []
    for rep in range(no_repetitions):
        new_counts = pick_new_sample(count_list)
        mean_N, var_N = get_meanvar(new_counts)
        if var_N >= mean_N:
            new_bias = compute_bias(mean_N, var_N, sigDM2=sigDM2)
        else:
            new_bias = 0
        bias_set.append(new_bias)
    return bias_set

def plot_hist_setbins(dataset, plot_filename, bin_range, binwidth, xlabel='x', ylabel='y', legend=False, label='data', x_range=None, y_range=None, line_colour='green', fill_colour='#fffdc9'):
    bins = np.arange(bin_range[0], bin_range[1], binwidth)
    plt.hist(dataset, bins=bins, histtype='stepfilled', color=fill_colour)
    plt.hist(dataset, bins=bins, histtype='step', color=line_colour, label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if not x_range == None:
        plt.xlim(x_range)
    if not y_range == None:
        plt.xlim(y_range)
    if legend:
        plt.legend()

    plt.savefig(plot_filename)
    plt.cla()

    return None

def plot_pdf_hist(dataset, plot_filename, bin_range, binwidth, xlabel='x', ylabel='y', legend=False, label='data', x_range=None, y_range=None, line_colour='green', fill_colour='#adf0a7'):
    bins = np.arange(bin_range[0], bin_range[1], binwidth)
    plt.hist(dataset, bins=bins, normed=True, histtype='stepfilled', color=fill_colour)
    plt.hist(dataset, bins=bins, normed=True, histtype='step', color=line_colour, label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if not x_range == None:
        plt.xlim(x_range)
    if not y_range == None:
        plt.xlim(y_range)
    if legend:
        plt.legend()

    plt.savefig(plot_filename)
    plt.cla()

    return None

def plot_bias_hist(bias_set, plot_filename, show=True, plot_title='Set of galaxy biases calculated from MC bootstrapping method'):
    """Plots a histogram of the biases obtained

    Parameters
    ----------
    bias_set : list
        The bias values obtained

    """
    Nbins = 25
    plt.hist(bias_set, bins=Nbins)
    plt.title(plot_title)
    plt.xlabel('bias')
    plt.ylabel('counts')
    plt.savefig(plot_filename)
    if show:
        plt.show()
    else:
        plt.cla()

if __name__=='__main__':
    from sys import argv
    script, results_dir = argv
    count_file = results_dir + 'count_data.dat'
    bias_set = MC_bootstrap(count_file, 1000)
    print "Mean:  %f    StDev:  %f" % (np.mean(bias_set), np.std(bias_set))
    plot_bias_hist(bias_set, results_dir + 'bias_error.png', show=True)
