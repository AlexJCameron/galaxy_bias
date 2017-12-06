import numpy as np
import read_counts
import bootstrap

# USAGE: python bias.py /dir/dir/results_dir/ 0.01234
#
# argv inputs are directory of results (containing count_data.dat) and value for sigma(DM)^2

if __name__=='__main__':
    # We'll take sigma(DarkMatter)**2 as 0.012333 - see Trenti & Stiavelli (2008)
    # sigDM2 = 0.012244 # Mean zb: 2.017586  zb int: 0.51441
    # sigDM2 = 0.014124 # Mean zb: 1.865264  zb int: 0.461496

    from sys import argv
    script, results_dir, sig_str = argv
    sigDM2 = float(sig_str)
    count_file = results_dir + 'count_data.dat'
    bias_filename = results_dir + 'bias.txt'

    early_list, late_list = read_counts.read_multi_type(count_file)
    data_dict = {
    'early':early_list,
    'late':late_list
    }
    types = ['early', 'late']
    bias_results = open(bias_filename, 'w')

    for tb in types:
        log1 = 'For %s type:' % tb
        print log1
        bias_results.write(log1 + '\n')

        mean_N, var_N = np.mean(data_dict[tb]), np.var(data_dict[tb])
        bias = bootstrap.compute_bias(mean_N, var_N, sigDM2=sigDM2)

        log2 = "Bias:  %f" % bias
        print log2
        bias_results.write(log2 + '\n')

        bias_set = bootstrap.MC_bootstrap_list(data_dict[tb], 1000, sigDM2=sigDM2)


        log3 = '\nBootstrapping bias set:\nMean:  %f    StDev:  %f' % (np.mean(bias_set), np.std(bias_set))
        print log3
        print '\n\n'
        bias_results.write(log3 + '\n\n\n')

        hist_filename = results_dir + 'bias_error_%s.eps' % tb
        pdf_filename = results_dir + 'bias_error_pdf_%s.eps' % tb

        bootstrap.plot_hist_setbins(bias_set, hist_filename, (0.,6.), 0.2, xlabel='$b$', ylabel='count', x_range=(0.,6.))
        bootstrap.plot_pdf_hist(bias_set, pdf_filename, (0.,6.), 0.2, xlabel='$b$', ylabel='$P(b)$', x_range=(0.,6.))
