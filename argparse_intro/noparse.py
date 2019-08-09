import pickle

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stat

#dataname = 'data01.pkl'
#dataname = 'data02.pkl'
dataname = 'data03.pkl'
#dataname = 'data04.pkl'
#dataname = 'data05.pkl'

nsamp = 1000
xlabel = 'this is an x-label'
ylabel = 'this is a y-label'
title = dataname.split('.')[0]
savename = 'img/output.pdf'

with open('data/{}'.format(dataname), 'rb') as f:
    model = pickle.load(f)

samples = np.linspace(0, 1, num=nsamp)

fig, ax = plt.subplots()
ax.plot(model.pdf(samples))
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
ax.set_title(title)

fig.savefig(savename, bbox_inches='tight')
