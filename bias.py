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
    bias_filename = results_dir + 'bias.txt'
    count_types = ['WhtCount', 'SegCount']

    count_data = read_counts.get_counts_data(count_file)
    bias_results = open(bias_filename, 'w')

    for count_type in count_types:
        log1 = 'For %s:' % count_type
        print log1
        bias_results.write(log1 + '\n')

        mean_N, var_N = read_counts.counts_meanvar(count_data, count_type=count_type)
        bias = bootstrap.compute_bias(mean_N, var_N, sigDM2=sigDM2)

        log2 = "Bias:  %f" % bias
        print log2
        bias_results.write(log2 + '\n')

        bias_set = bootstrap.MC_bootstrap(count_file, 1000, sigDM2=sigDM2, count_type=count_type)

        log3 = '\nBootstrapping bias set:\nMean:  %f    StDev:  %f' % (np.mean(bias_set), np.std(bias_set))
        print log3
        print '\n\n'
        bias_results.write(log3 + '\n\n\n')

        plot_filename = results_dir + 'bias_error_%s.png' % count_type
        bootstrap.plot_bias_hist(bias_set, plot_filename)
