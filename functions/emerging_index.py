import numpy as np

def add_emerging_index(df, col_name='emerging_index', n_days=4, min_deaths=20, new_deaths=True):

    # TODO: stability of new_deaths vs. cumulative
    if new_deaths:
        index = 'new_deaths'
        # compute new deaths
        df['new_deaths'] = (df['deaths'] - df['tot_deaths']).apply(
            lambda x: np.array(
                [x[-(i+1)] - x[-i] for i in range(n_days)]
            )
        )
    else:
        index = 'deaths'

    # TODO: stability of n_days
    def compute_growth_factor(x, n_days=4):
        past_n_days = x[-n_days:]
        growth_factor = (past_n_days / np.insert(x[-4:-1], 0, 1))[-(n_days-1):]
        return np.mean(growth_factor) + np.cov(np.arange(3), growth_factor)[0][1]

    # the emerging_index scales by log(pop_density) * median_age /
    # (# hospitals + 1) / log(tot_deaths)
    df['emerging_index'] = df[index].apply(lambda x: compute_growth_factor(x)) * \
        np.log(df['PopulationDensityperSqMile2010']) * df['MedianAge2010'] / \
        (df['#Hospitals'] + 1) / np.log(df['tot_deaths'] + 1)

    # scale to be between 0 and 1
    df['emerging_index'] = (df['emerging_index'] - df['emerging_index'].min()) / \
        (df['emerging_index'].max() - df['emerging_index'].min())

    # TODO: look into stability of this threshold
    # 0 out any county with less than min_deaths
    df['emerging_index'] = (1 - (df['tot_deaths'] < min_deaths)) * df['emerging_index']

    return None
