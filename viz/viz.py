import seaborn as sns
import matplotlib.pyplot as plt

def corrplot(df, SIZE=8):
    # sns.set(style="white")

    # Compute the correlation matrix
    corrs = df.corr(method='spearman')

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(10, 220, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    plt.figure(figsize=(SIZE, SIZE), dpi=300)
    sns.heatmap(corrs, cmap=cmap, vmax=1, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
    # sns.clustermap(corr, cmap=cmap, vmax=1, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.tight_layout()
