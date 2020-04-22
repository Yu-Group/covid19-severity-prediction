import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
cs = ['#6E8E96', '#D3787D', '#AC3931']

def corrplot(df, SIZE=8):
    # sns.set(style="white")

    # Compute the correlation matrix
    corrs = df.corr(method='spearman')

    mask = np.triu(np.ones_like(corrs, dtype=np.bool))
    
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(10, 220, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    plt.figure(figsize=(SIZE, SIZE), dpi=150)
    sns.heatmap(corrs, cmap=cmap, mask=mask, center=0, 
                square=True, linewidths=0, cbar_kws={"shrink": .5})
    # sns.clustermap(corr, cmap=cmap, vmax=1, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.tight_layout()

def plot_scatter(x, y, c, s, xlab: str, ylab: str, colorlab: str,
                 sizelab: str, markersize_rescaling: int, figsize=(7, 3)):
    '''
    Params
    ------
    markersize_rescaling: 
    '''
    fig, ax = plt.subplots(dpi=500, figsize=figsize)
    scatter = ax.scatter(x, y, c=c, s=s, alpha=1)
    plt.yscale('symlog')
    plt.xscale('symlog')

    # produce a legend with the unique colors from the scatter
    leg_els = [Line2D([0], [0], marker='o', color='w', label='High', markerfacecolor=cs[2], markersize=6),
               Line2D([0], [0], marker='o', color='w', label='Medium', markerfacecolor=cs[1], markersize=6),
               Line2D([0], [0], marker='o', color='w', label='Low', markerfacecolor=cs[0], markersize=6)]

    # leg_els = scatter.legend_elements()
    # legend1 = ax.legend(*leg_els, loc="upper left", title="Severity Index")
    legend1 = ax.legend(handles=leg_els, loc="upper left", title=colorlab, fontsize=9)
    ax.add_artist(legend1)

    # produce a legend with a cross section of sizes from the scatter
    handles, labels = scatter.legend_elements(prop="sizes", alpha=1)
    l2 = []
    for i in range(len(labels)):
        s = labels[i]
        num = markersize_rescaling * int(s[s.index('{') + 1: s.index('}')])
        l2.append('$\\mathdefault{' + str(num) + '}$')
    legend2 = ax.legend(handles, l2, loc="lower right", title=sizelab)
    plt.xlabel(xlab)
    plt.ylabel(ylab)