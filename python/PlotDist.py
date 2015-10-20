
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# Initial script to plot things to get a feel for how well the #
# hacked weighting scheme is working.                          #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

import numpy as np
from root_numpy import root2array
import matplotlib.pyplot as plt
from MuEvtWeight import MuEvtWeightTool

# Set Paths here
mu_effa_path = "data/total_effarea.pkl"
mu_data_path0 = "trees/NuGen_11069_Sep14_L3Applied.root"
mu_data_path1 = "trees/NuGen_11070_Sep14_L3Applied.root"


# Create a weight tool
w_tool = MuEvtWeightTool(mu_effa_path)

# Load the data
mu_branches = ['nuE','nuZen',"muE","muZen",'mu_Ei','mu_Ef','mu_dE','InteractionType',
               'trunc_bins_E','trunc_doms_E',
               'OneWeight','NEvents']
mu_sel = "InteractionType == 1 && cos(muZen) < 0.2&&mu_dE > 0 && trunc_bins_E > 0 && trunc_doms_E>0"
mu_data0 = root2array(filenames = mu_data_path0,
                     treename = "tree",
                     selection = mu_sel,
                     branches = mu_branches)
mu_data1 = root2array(filenames = mu_data_path1,
                     treename = "tree",
                     selection = mu_sel,
                     branches = mu_branches)

# Loop over the data, get the weights and then plot
mu_weights0 = np.empty(len(mu_data0['nuE']))
for i in range(len(mu_data0['nuE'])):
    mu_weights0[i] = w_tool.getMuW( mu_data0['nuE'][i], 
                                    mu_data0['OneWeight'][i],
                                    mu_data0['NEvents'][i] * 961)

mu_weights1 = np.empty(len(mu_data1['nuE']))
for i in range(len(mu_data1['nuE'])):
    mu_weights1[i] = w_tool.getMuW( mu_data1['nuE'][i], 
                                    mu_data1['OneWeight'][i],
                                    mu_data1['NEvents'][i] * 999)

mu_weights0_inc30 = np.empty(len(mu_data0['nuE']))
for i in range(len(mu_data0['nuE'])):
    mu_weights0_inc30[i] = w_tool.getMuW( mu_data0['nuE'][i], 
                                          mu_data0['OneWeight'][i],
                                          mu_data0['NEvents'][i] * 961,
                                          True,1.3)
    
mu_weights1_inc30 = np.empty(len(mu_data1['nuE']))
for i in range(len(mu_data1['nuE'])):
    mu_weights1_inc30[i] = w_tool.getMuW( mu_data1['nuE'][i], 
                                          mu_data1['OneWeight'][i],
                                          mu_data1['NEvents'][i] * 999,
                                          True,1.3)
    
mu_weights0_inc60 = np.empty(len(mu_data0['nuE']))
for i in range(len(mu_data0['nuE'])):
    mu_weights0_inc60[i] = w_tool.getMuW( mu_data0['nuE'][i], 
                                          mu_data0['OneWeight'][i],
                                          mu_data0['NEvents'][i] * 961,
                                          True,1.6)
    
mu_weights1_inc60 = np.empty(len(mu_data1['nuE']))
for i in range(len(mu_data1['nuE'])):
    mu_weights1_inc60[i] = w_tool.getMuW( mu_data1['nuE'][i], 
                                          mu_data1['OneWeight'][i],
                                          mu_data1['NEvents'][i] * 999,
                                          True,1.6)
    

# Concat the data
mu_data = np.concatenate((mu_data0, mu_data1),axis=1)
mu_weights = np.concatenate((mu_weights0, mu_weights1),axis=1)
mu_weights_inc30 = np.concatenate((mu_weights0_inc30, mu_weights1_inc30),axis=1)
mu_weights_inc60 = np.concatenate((mu_weights0_inc60, mu_weights1_inc60),axis=1)


# Plots
nbins = 50

plt.hist(np.log10(mu_data['trunc_bins_E']), weights = mu_weights,
         bins = nbins,
         histtype = 'step',
         range = (2,7),
         label = "truncated bins",
         color='black',
         log = True)

plt.hist(np.log10(mu_data['trunc_bins_E']), weights = mu_weights_inc30,
         bins = nbins,
         histtype = 'step',
         range = (2,7),
         label = "truncated bins +30%",
         color='r',
         log = True)

plt.hist(np.log10(mu_data['trunc_bins_E']), weights = mu_weights_inc60,
         bins = nbins,
         histtype = 'step',
         range = (2,7),
         label = "truncated bins +60%",
         color='b',
         log = True)

plt.xlabel(r'log$_{10}$(Energy Proxy)')
plt.ylabel('Events / year / bin')
plt.grid()
#plt.ylim([1e-6,1e6])
plt.tight_layout()
plt.legend(loc='best')
#plt.savefig('plots/IncreasePeVEffArea_scale10.png')
plt.show()
