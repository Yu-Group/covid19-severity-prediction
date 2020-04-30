import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from adjustText import adjust_text
import datetime
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
    fig, ax = plt.subplots(dpi=500, figsize=figsize, facecolor='w')
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
    


def plot_forecasts(dd, target='deaths', days_in_future=5, death_thresh=0):
    # cs = sns.diverging_palette(20, 220, n=NUM_COUNTIES)
    def nonzero_len(l):
        return len([x for x in l if x > death_thresh])
    lens = dd['deaths'].apply(nonzero_len)
    cs = sns.color_palette("husl", dd.shape[0])
    labs = []
    lab_ys = []
    
    num = max(lens)
    end = num + days_in_future
    d = datetime.datetime.today()
    d2 = d + datetime.timedelta(days=days_in_future)
    dinit = d + datetime.timedelta(days=-num)
    xticks = [0, num - 1, end - 1]
    xlabs = [f'{dinit.month}/{dinit.day}', f'{d.month}/{d.day}', f'{d2.month}/{d2.day}']
    
    for i in range(dd.shape[0]):
        row = dd.iloc[i]

        deaths = row.deaths[-num:]
        
        intervals = row[f'Predicted {target.capitalize()} Intervals']
        lower = [deaths[-1]] + [x[0] for x in intervals][:days_in_future]
        upper = [deaths[-1]] + [x[1] for x in intervals][:days_in_future]
        preds = [deaths[-1]] + [row[f'Predicted {target.capitalize()} {i}-day'] for i in range(1, days_in_future + 1)]
        plt.plot(np.arange(num), deaths, alpha=1, color=cs[i])
        plt.fill_between(np.arange(num - 1, end), lower, upper, color=cs[i], alpha=0.1)
        plt.plot(np.arange(num - 1, end), preds, linestyle='dotted', alpha=1, color=cs[i])
        plt.ylabel('Cumulative deaths')
        plt.xlabel(f'Date')
        plt.xticks(xticks, xlabs, rotation=0)
        plt.xlim(right=end * 1.25) # extend lim to make space for labels
        labs.append(row['CountyName'] + ', ' + row['StateName'])
        lab_ys.append(preds[-1])
    
    # put on labels    
    texts = []
    for i in range(len(labs)):
        texts.append(plt.text(end, 
                              lab_ys[i],
                              labs[i],
                              color=cs[i], fontsize=8))
        
    # make sure labels don't overlap
    adjust_text(texts, only_move={'points': 'y',
                                  'text': 'y',
                                  'objects': 'y'}) #, arrowprops=dict(arrowstyle="->", color='r', lw=0.5))

