import numpy as np
import read_counts
import bootstrap

if __name__=='__main__':
    # We'll take sigma(DarkMatter)**2 as 0.012333 - see Trenti & Stiavelli (2008)
    sigDM2 = 0.012333

    count_file = '/home/alexc/Documents/l_proj/photoz/borgz8_results/nodust_count_data.dat'
    count_type = 'WhtCount'

    count_data = read_counts.get_counts_data(count_file)
    mean_N, var_N = read_counts.counts_meanvar(count_data, count_type=count_type)

    bias = bootstrap.compute_bias(mean_N, var_N, sigDM2=sigDM2)
    print "Bias:  %f" % bias
