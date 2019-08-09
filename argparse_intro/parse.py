import argparse
import os
import pickle
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stat

parser = argparse.ArgumentParser()

parser.add_argument('infile',
                    help='Path to input file.',
                    type=str,
)
parser.add_argument('-o', '--outfile',
                    help=('Name of output file. By default the file is saved to the '
                          '`img` directory. If no name is supplied, then a name is '
                          'assigned based on the input data and a timestamp is '
                          'appended. If a path is supplied, then the output file is'
                          'saved there rather than the `img` directory.'),
                    type=str,
                    default=None,
)
parser.add_argument('-n', '--nsamp',
                    help=('The number of samples to draw from the model distribution. '
                          'Default is 100.'),
                    default=100,
                    type=int,
)
parser.add_argument('-e', '--ext',
                    help='File type of the output figure. Default is pdf.',
                    type=str,
                    choices=['pdf', 'png'],
                    default='pdf',
)
parser.add_argument('--xlabel',
                    help='Label for the x-axis. By default there is no x-label',
                    type=str,
                    default=None,
)
parser.add_argument('--ylabel',
                    help='Label for the y-axis. By default there is no y-label',
                    type=str,
                    default=None,
)
parser.add_argument('--datalabel',
                    help=('Label for the data, which will appear in the legend if '
                          'it is enabled. By default the label is \'data\''),
                    type=str,
                    default=None,
)
parser.add_argument('-l', '--legend',
                    help=('Draw a legend on the figure. By default the legend is '
                          'omitted. The legend is drawn according to the matplotlib '
                          '`loc=\'best\'` criteria.'),
                    default=False,
                    action='store_true',
)
meg = parser.add_mutually_exclusive_group()
meg.add_argument('--nothing',
                 help='Annotate the figure as a \'Nothing\'',
                 default=False,
                 action='store_true',
)
meg.add_argument('--something',
                 help='Annotate the figure as a \'Something\'',
                 default=False,
                 action='store_true',
)
args = parser.parse_args()

basename = os.path.basename(args.infile).split()[0]

if args.outfile is None:
    args.outfile = basename + time.strftime('_%Y%m%d_%H%M%S') + '.' + args.ext
if not (os.path.sep in args.outfile):
    args.outfile = os.path.join(os.getcwd(), 'img', args.outfile)
if not (args.outfile.endswith('.pdf') or args.outfile.endswith('.png')):
    args.outfile += '.' + args.ext

if args.xlabel is None:
    args.xlabel = ''
if args.ylabel is None:
    args.ylabel = ''
if args.datalabel is None:
    args.datalabel = 'data'

annotation = None
if args.nothing:
    annotation = 'Nothing'
if args.something:
    annotation = 'Something'

try:
    with open(args.infile, 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print('Could not find file "{}"'.format(args.infile))
    print('Exiting with status 1')
    sys.exit(1)

samples = np.linspace(0, 1, num=args.nsamp)
distribution = model.pdf(samples)

fig, ax = plt.subplots()
ax.plot(distribution, label=args.datalabel)
ax.set_xlabel(args.xlabel)
ax.set_ylabel(args.ylabel)
if args.legend:
    ax.legend(loc='best')
if isinstance(annotation, str):
    xpos = np.argmax(distribution)
    ypos = np.max(distribution)
    ax.annotate(annotation, xy=(xpos, ypos), xytext=(xpos+5, ypos*1.25), arrowprops={'arrowstyle':'fancy'})
    ax.set_ylim(ymax=ypos*1.4)

fig.savefig(args.outfile, bbox_inches='tight')

##dataname = 'data01.pkl'
##dataname = 'data02.pkl'
#dataname = 'data03.pkl'
##dataname = 'data04.pkl'
##dataname = 'data05.pkl'
#
#nsamp = 1000
#xlabel = 'this is an x-label'
#ylabel = 'this is a y-label'
#title = dataname.split('.')[0]
#savename = 'img/output.pdf'
#
#with open('data/{}'.format(dataname), 'rb') as f:
#    model = pickle.load(f)
#
#samples = np.linspace(0, 1, num=nsamp)
#
#fig, ax = plt.subplots()
#ax.plot(model.pdf(samples))
#ax.set_xlabel(xlabel)
#ax.set_ylabel(ylabel)
#ax.set_title(title)
#
#fig.savefig(savename, bbox_inches='tight')
