from unittest import result
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker


def convert_fold_to_log_fold(temp_fold):
    """
    Custom conversion to the typical log fold change from earlier implementation.
    Currently unused.
    """
    if temp_fold > 0:
        return np.log2(temp_fold)
    elif temp_fold < 0:
        return np.log2(abs(1 / temp_fold))


def coerce_our_structure_to_plotly_volcano(
    temp_fold_panda, temp_signifigance_panda, temp_metabolite
):
    """
    Coerces our input panda structure to the structures that Plotly's dash-bio expects
    """

    # generally, we only want to plot the upper triangle from our comparison matrix
    # because the matrix is anti-symmetric
    if only_plot_upper_triangle == True:
        m, n = temp_fold_panda.shape
        temp_fold_panda[:] = np.where(
            np.arange(m)[:, None] >= np.arange(n), np.nan, temp_fold_panda
        )
        temp_signifigance_panda[:] = np.where(
            np.arange(m)[:, None] >= np.arange(n), np.nan, temp_signifigance_panda
        )

    # "pivot" multiindex to long list
    temp_fold_panda = temp_fold_panda.stack().stack().stack()
    # the same strings were column and index labels - this causes problems with stacking so we rename
    temp_fold_panda.index.rename(
        [
            "organ_from",
            "species_from",
            "disease_from",
            "disease_to",
            "species_to",
            "organ_to",
        ],
        inplace=True,
    )
    temp_fold_panda = temp_fold_panda.reset_index()
    # declare a new column as a tuple from the previous multiindex
    temp_fold_panda["from"] = temp_fold_panda[
        ["organ_from", "species_from", "disease_from"]
    ].apply(tuple, axis="columns")
    # declare a new column as a tuple from the previous multiindex
    temp_fold_panda["to"] = temp_fold_panda[
        ["organ_to", "species_to", "disease_to"]
    ].apply(tuple, axis="columns")
    # remove old multiindex
    temp_fold_panda = temp_fold_panda.drop(
        [
            "organ_from",
            "species_from",
            "disease_from",
            "disease_to",
            "species_to",
            "organ_to",
        ],
        axis="columns",
    )
    # rename column to match plotly convention "fold"
    temp_fold_panda.rename({0: "fold"}, axis="columns", inplace=True)

    # the same logic as above but on the statistical significance panda
    temp_signifigance_panda = temp_signifigance_panda.stack().stack().stack()
    temp_signifigance_panda.index.rename(
        [
            "organ_from",
            "species_from",
            "disease_from",
            "disease_to",
            "species_to",
            "organ_to",
        ],
        inplace=True,
    )
    temp_signifigance_panda = temp_signifigance_panda.reset_index()
    temp_signifigance_panda["from"] = temp_signifigance_panda[
        ["organ_from", "species_from", "disease_from"]
    ].apply(tuple, axis="columns")
    temp_signifigance_panda["to"] = temp_signifigance_panda[
        ["organ_to", "species_to", "disease_to"]
    ].apply(tuple, axis="columns")
    temp_signifigance_panda = temp_signifigance_panda.drop(
        [
            "organ_from",
            "species_from",
            "disease_from",
            "disease_to",
            "species_to",
            "organ_to",
        ],
        axis="columns",
    )
    temp_signifigance_panda.rename({0: "signifigance"}, axis="columns", inplace=True)

    # concatenate the results of biological and significance pandas
    temp_fold_panda["signifigance"] = temp_signifigance_panda["signifigance"]
    # snap from dash plotly docs. used in genomics.
    temp_fold_panda["snap"] = (
        "from: "
        + temp_fold_panda["from"].astype(str)
        + " to: "
        + temp_fold_panda["to"].astype(str)
    )
    temp_fold_panda.drop(["from", "to"], inplace=True, axis="columns")
    temp_fold_panda["metabolite"] = temp_metabolite

    return temp_fold_panda


if __name__ == "__main__":

    # parameters for this invocation of the script
    fold_type = "fold_change_median_intensity"
    signifigance_type = "signifigance_mannwhitney"
    fold_cutoff = 2
    signifigance_cutoff = 0.01
    only_plot_upper_triangle = True
    input_panda_address = "../../results/0/step_6_b_generate_signifigance_test_matrices/binvestigate_with_signifigance_matrices.bin"

    full_data_panda = pd.read_pickle(input_panda_address)
    yes_signifigance_yes_fold = list()
    yes_signifigance_no_fold = list()
    no_signifigance_no_fold = list()
    no_signifigance_yes_fold = list()
    metabolite_list = list()
    total_x_position_list = list()
    total_y_position_list = list()

    # the overall logic is to iterate over every row in the panda and extract the embedded comparison panda.
    # each row represents a compound
    # for each row, there is an embedded panda that contains the metadata group comparisons
    # this is too sophisticated to be readily vectorized, but we vectorize work on the embedded panda
    # in the above function 'coerce_our_structure_to_plotly_volcano'
    for index, series in full_data_panda.iterrows():
        print(index)
        fold_panda = full_data_panda.at[index, fold_type]
        signifigance_panda = full_data_panda.at[index, signifigance_type]
        metabolite = full_data_panda.at[index, "name"]
        result_panda = coerce_our_structure_to_plotly_volcano(
            fold_panda, signifigance_panda, metabolite
        )

        # getting the results for the full matrix and printing only the right hand side
        # is not the same thing as getting the results for the upper triangle only and printing both sides
        if only_plot_upper_triangle == False:
            result_panda = result_panda.loc[result_panda["fold"] > 0]

        metabolite_list.append(metabolite)

        if index == 0:
            total_panda = result_panda[["fold", "signifigance"]].copy(deep=True)
        elif index != 0:
            print("here")
            total_panda = total_panda.append(result_panda[["fold", "signifigance"]])

    # after obtaining the transformation from teh embedded comparison panda
    # we perform some quality-control and then count the results
    if only_plot_upper_triangle == False:
        total_panda = total_panda.loc[total_panda["fold"] > 0]

    # we choose to represent the significance on a log scale
    total_panda["signifigance"] = np.log(total_panda["signifigance"])
    total_panda["signifigance"] = total_panda["signifigance"].mul(-1)

    # create a histogram of the fold and significance panda for a heatmap
    my_histogram, x_edges, y_edges = np.histogram2d(
        total_panda["fold"], total_panda["signifigance"], bins=[100, 100]
    )
    my_histogram = np.log10(my_histogram)
    my_histogram = np.where(np.isfinite(my_histogram), my_histogram, 0)
    extent = [x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]]

    # create figure from out histogram
    fig, ax = plt.subplots()
    divider = make_axes_locatable(ax)
    plt.title("Mann-Whitney U-Test p-values vs. Fold Change of Medians")
    plt.ylabel("-log10(p-value)")
    plt.xlabel("-log2(fold-change)")
    tick_spacing = 2
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    if only_plot_upper_triangle == True:
        plt.vlines(x=2, ymin=0, ymax=750, colors="g", linewidth=1)
        plt.hlines(y=2, xmin=-20, xmax=20, colors="g", linewidth=1)
        plt.vlines(x=-2, ymin=0, ymax=750, colors="g", linewidth=1)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    image = ax.imshow(
        my_histogram.T, extent=extent, origin="lower", aspect="auto", cmap="magma"
    )
    fig.colorbar(image, cax=cax, orientation="vertical")
    plt.savefig("./median.png")

    # after creation of the figure
    # we obtain value for a "confusion matrix-like" plot to examine how many results were significant
    signifigance_cutoff = -1 * np.log(signifigance_cutoff)
    yes_signifigance_yes_fold = len(
        total_panda.loc[
            (total_panda["signifigance"] <= signifigance_cutoff)
            & (total_panda["fold"].abs() >= fold_cutoff)
        ]
    )
    yes_signifigance_no_fold = len(
        total_panda.loc[
            (total_panda["signifigance"] <= signifigance_cutoff)
            & (total_panda["fold"].abs() < fold_cutoff)
        ]
    )
    no_signifigance_no_fold = len(
        total_panda.loc[
            (total_panda["signifigance"] > signifigance_cutoff)
            & (total_panda["fold"].abs() < fold_cutoff)
        ]
    )
    no_signifigance_yes_fold = len(
        total_panda.loc[
            (total_panda["signifigance"] > signifigance_cutoff)
            & (total_panda["fold"].abs() >= fold_cutoff)
        ]
    )

    print("yes_signifigance_yes_fold " + str((yes_signifigance_yes_fold)))
    print("yes_signifigance_no_fold " + str((yes_signifigance_no_fold)))
    print("no_signifigance_no_fold " + str((no_signifigance_no_fold)))
    print("no_signifigance_yes_fold " + str((no_signifigance_yes_fold)))
    print(len(full_data_panda.at[0, "species"]))
