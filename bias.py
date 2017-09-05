import numpy as np
import read_counts
import bootstrap

if __name__=='__main__':
    # We'll take sigma(DarkMatter)**2 as 0.012333 - see Trenti & Stiavelli (2008)
    # sigDM2 = 0.012333 # Mean zb: 2.019475  zb int: 0.50958
    sigDM2 = 0.012244 # Mean zb: 2.017586  zb int: 0.51441
    # sigDM2 = 0.014124 # Mean zb: 1.865264  zb int: 0.461496

    from sys import argv
    script, results_dir = argv
    count_file = results_dir + 'count_data.dat'
    count_type = 'WhtCount'

    count_data = read_counts.get_counts_data(count_file)
    mean_N, var_N = read_counts.counts_meanvar(count_data, count_type=count_type)

    bias = bootstrap.compute_bias(mean_N, var_N, sigDM2=sigDM2)
    print "Bias:  %f" % bias
