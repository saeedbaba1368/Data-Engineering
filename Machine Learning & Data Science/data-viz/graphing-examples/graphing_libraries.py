import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import axes3d
import mplcursors

import pandas as pd
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import axes3d

import ipywidgets as widgets
import seaborn as sns


# If widgets are not rendering or interactivity is not working
# https://github.com/jupyterlab/jupyterlab/issues/12580

# using plotly
# https://saturncloud.io/blog/troubleshooting-plotly-chart-not-showing-in-jupyter-notebook/


class ThreeDPlotter:
    """Basic Usage
    Generate random data

    plotter = ThreeDPlotter( dataframe=df)
    plotter.plot_3d_bar(columns_to_include=['Column1', 'Column2'], years_subset=[2010, 2011, 2013, 2014], growth_rate=0.05)
    plotter.plot_3d_line(columns_to_include=['Column1', 'Column2', 'Column3'], add_average=True, scale_factor=None, growth_rate=0.05,  show_original=True, years_subset=None)
    plotter.plot_3d_stem(columns_to_include=['Column1', 'Column2', 'Column3'], add_average=False, scale_factor=None, show_original=True, years_subset=None, growth_rate=0.05)
    """

    def __init__(self, dataframe, kind = "By Column"):
        self.dataframe = dataframe
        self.kind = kind

    def plot_3d_line(
        self,
        columns_to_include=None,
        add_average=False,
        scale_factor=None,
        growth_rate=None,
        show_original=False,
        years_subset=None,
    ):
        """
        Generate a 3D line plot of time series data.

        Parameters:
        - columns_to_include: list, optional
            List of column names to include in the plot. If None, all columns in the dataframe are included.
        - add_average: bool, optional
            If True, add a line for the average value of each column.
        - scale_factor: float, optional
            Factor to scale the values by. If None, no scaling is applied.
        - growth_rate: float, optional
            Compound growth rate to apply to the values. If provided, a growth rate line is added to the plot.
        - show_original: bool, optional
            If True, show the original values in addition to any scaled or growth rate values.
        - years_subset: list, optional
            List of years to include in the plot. If None, all years in the dataframe are included.

        Returns:
        None
        """
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection="3d")

        if years_subset is None:
            years_subset = self.dataframe.index

        if columns_to_include is None:
            columns_to_include = self.dataframe.columns

        for i, column in enumerate(columns_to_include):
            if column in self.dataframe.columns:
                values = self.dataframe[column].loc[years_subset].values

                if show_original:
                    ax.plot(
                        years_subset,
                        np.full_like(years_subset, i),
                        values,
                        label=f"{column} Original",
                        linestyle="-",
                        color="green",
                    )

                if (growth_rate is not None) and (growth_rate != 0.0):
                    t = np.arange(len(years_subset))
                    growth_values = values * (1 + growth_rate) ** t
                    ax.plot(
                        years_subset,
                        np.full_like(years_subset, i),
                        growth_values,
                        linestyle="-",
                        color="orange",
                    )  # label=f'{column} Growth Rate'

                if (scale_factor is not None) and (scale_factor != 0.0):
                    scaled_values = values * scale_factor
                    ax.plot(
                        years_subset,
                        np.full_like(years_subset, i),
                        scaled_values,
                        linestyle="-",
                        color="blue",
                    )  # label=f'{column} Scaled'

                if add_average:
                    average_value = values.mean()
                    ax.plot(
                        years_subset,
                        np.full_like(years_subset, i),
                        np.full_like(years_subset, average_value),
                        linestyle="--",
                        color="black",
                    )  # label=f'{column} Average'

        ax.set_xlabel("Year")
        ax.set_ylabel("Columns")
        ax.set_zlabel("Values")
        ax.set_title(f"{self.kind}")

        # Set y-axis ticks and labels using column names
        ax.set_yticks(np.arange(len(columns_to_include)))
        ax.set_yticklabels(columns_to_include)
        ax.legend(
            loc="upper left",
            bbox_to_anchor=(3.5, 3.5),
            bbox_transform=fig.transFigure 
        
        )
        #ax.legend()
        plt.show()

    def plot_3d_bar(
        self,
        columns_to_include=None,
        scale_factor=None,
        show_original=False,
        years_subset=None,
        growth_rate=None,
    ):
        """
        Generate a 3D bar chart of time series data.

        Parameters:
        - columns_to_include: list, optional
            List of column names to include in the plot. If None, all columns in the dataframe are included.
        - scale_factor: float, optional
            Factor to scale the values by. If None, no scaling is applied.
        - show_original: bool, optional
            If True, show the original values in addition to any scaled or growth rate values.
        - years_subset: list, optional
            List of years to include in the plot. If None, all years in the dataframe are included.
        - growth_rate: float, optional
            Compound growth rate to apply to the values. If provided, a growth rate bar is added to the plot.

        Returns:
        None
        """
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection="3d")

        if years_subset is None:
            years_subset = self.dataframe.index

        if columns_to_include is None:
            columns_to_include = self.dataframe.columns

        values = np.array(self.dataframe[columns_to_include].loc[years_subset].values)

        xpos, ypos = np.meshgrid(
            range(len(years_subset)), range(len(columns_to_include)), indexing="ij"
        )
        xpos = xpos.ravel()
        ypos = ypos.ravel()
        zpos = np.zeros_like(xpos)

        dx = dy = 0.4  # Adjust the width of the bars
        dz_original = values.ravel()

        if (growth_rate is not None) and (growth_rate != 0.0):
            t = np.arange(len(years_subset))
            growth_values = values * (1 + growth_rate) ** t[:, np.newaxis]
            dz_growth = growth_values.ravel()

            colors_growth = cm.Paired(np.linspace(0, 1, len(columns_to_include)))

            for i, (column, color_growth) in enumerate(
                zip(columns_to_include, colors_growth)
            ):
                ax.bar3d(
                    xpos[i :: len(columns_to_include)],
                    ypos[i :: len(columns_to_include)] + dy,
                    zpos[i :: len(columns_to_include)],
                    dx,
                    dy,
                    dz_growth[i :: len(columns_to_include)],
                    shade=True,
                    color=color_growth,
                    label=f"{column} Growth Rate",
                )

        if (scale_factor is not None) and (scale_factor != 0.0):
            dz_scaled = values.ravel() * scale_factor
            colors_scaled = cm.Dark2(np.linspace(0, 1, len(columns_to_include)))

            for i, (column, color_scaled) in enumerate(
                zip(columns_to_include, colors_scaled)
            ):
                ax.bar3d(
                    xpos[i :: len(columns_to_include)],
                    ypos[i :: len(columns_to_include)] + dy,
                    zpos[i :: len(columns_to_include)],
                    dx,
                    dy,
                    dz_scaled[i :: len(columns_to_include)],
                    shade=True,
                    color=color_scaled,
                    label=f"{column} Scaled",
                )

        colors_original = cm.viridis(np.linspace(0, 1, len(columns_to_include)))

        for i, (column, color_original) in enumerate(
            zip(columns_to_include, colors_original)
        ):
            ax.bar3d(
                xpos[i :: len(columns_to_include)],
                ypos[i :: len(columns_to_include)],
                zpos[i :: len(columns_to_include)],
                dx,
                dy,
                dz_original[i :: len(columns_to_include)],
                shade=True,
                color=color_original,
                label=f"{column} Original",
            )

        ax.set_xlabel("Year")
        ax.set_ylabel("Columns")
        ax.set_zlabel("Values")
        ax.set_title(f"{self.kind}")

        ax.set_xticks(np.arange(len(years_subset)) + 0.4)
        ax.set_xticklabels(years_subset)
        ax.set_yticks(np.arange(len(columns_to_include)) + 0.4)
        ax.set_yticklabels(columns_to_include)

        ax.legend()
        plt.show()

    def plot_3d_stem(
        self,
        columns_to_include=None,
        add_average=False,
        scale_factor=None,
        show_original=False,
        years_subset=None,
        growth_rate=None,
    ):
        """
        Generate a 3D stem plot of time series data.

        Parameters:
        - columns_to_include: list, optional
            List of column names to include in the plot. If None, all columns in the dataframe are included.
        - add_average: bool, optional
            If True, add a line for the average value of each column.
        - scale_factor: float, optional
            Factor to scale the values by. If None, no scaling is applied.
        - show_original: bool, optional
            If True, show the original values in addition to any scaled or averaged values.
        - years_subset: list, optional
            List of years to include in the plot. If None, all years in the dataframe are included.
        - growth_rate: float, optional
            Compound growth rate to apply to the values. If provided, a growth rate line is added to the plot.

        Returns:
        None
        """
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection="3d")

        if years_subset is None:
            years_subset = self.dataframe.index

        if columns_to_include is None:
            columns_to_include = self.dataframe.columns

        for i, column in enumerate(columns_to_include):
            if column in self.dataframe.columns:
                values = self.dataframe[column].loc[years_subset].values

                if (growth_rate is not None) and (growth_rate != 0.0):
                    t = np.arange(len(years_subset))
                    growth_values = values * (1 + growth_rate) ** t
                    ax.stem(
                        years_subset,
                        np.full_like(years_subset, i),
                        growth_values,
                        label=f"{column} Growth Rate",
                        basefmt="k-",
                        linefmt="--",
                        markerfmt="o",
                    )

                if show_original:
                    ax.stem(
                        years_subset,
                        np.full_like(years_subset, i),
                        values,
                        label=f"{column} Original",
                        basefmt="k-",
                        linefmt="--",
                        markerfmt="o",
                    )

                if (scale_factor is not None) and (scale_factor != 0.0):
                    scaled_values = values * scale_factor
                    ax.plot(
                        years_subset,
                        np.full_like(years_subset, i),
                        scaled_values,
                        label=f"{column} Scaled",
                        linestyle="-",
                        color="blue",
                        marker="o",
                    )

                if add_average:
                    average_value = values.mean()
                    ax.plot(
                        years_subset,
                        np.full_like(years_subset, i),
                        np.full_like(years_subset, average_value),
                        linestyle="--",
                        color="red",
                        label=f"{column} Average",
                    )

        ax.set_xlabel("Year")
        ax.set_ylabel("Columns")
        ax.set_zlabel("Values")
        ax.set_title(f"{self.kind}")

        # Set y-axis ticks and labels using column names
        ax.set_yticks(np.arange(len(columns_to_include)))
        ax.set_yticklabels(columns_to_include)

        ax.legend()
        plt.show()


class TimeSeriesPlotter:
    def __init__(self, dataframe, kind = "Columns"):
        self.dataframe = dataframe
        self.kind = "Columns"

    def plot_interactive_time_series(
        self,
        columns_subset=None,
        years_subset=None,
        scale_factor=None,
        growth_rate=None,
        show_original=False,
        moving_average_window=None,
        plot_original_moving_average=False,
        plot_scaled_on_original=False,
        plot_growth_rate_moving_average=False,
        plot_growth_rate_on_original=False,
    ):
        """
        Plot interactive time series with optional scaling, growth rate, and moving average.

        Parameters:
            columns_subset (list, optional): List of columns to be plotted. Default is all columns in the dataframe.
            years_subset (list, optional): List of years to be plotted. Default is all years in the dataframe.
            scale_factor (float, optional): Factor to scale the values by. Default is None.
            growth_rate (float, optional): Compound growth rate to apply to the values. The formula used is:
                new_value = original_value * (1 + growth_rate)^t, where t is the number of periods.
                Default is None.
            show_original (bool, optional): Whether to show the original values. Default is True.
            moving_average_window (int, optional): Window size for calculating the moving average. Default is None.
            plot_original_moving_average (bool, optional): Whether to plot moving average and error bars for the original series. Default is False.
            plot_scaled_moving_average (bool, optional): Whether to plot moving average and error bars for the scaled series. Default is False.
            plot_scaled_on_original (bool, optional): Whether to plot the scaled series on the original plot. Default is False.

        Returns:
            None

        Basic Usage:

            ts_plotter = TimeSeriesPlotter(df)

            ts_plotter.plot_interactive_time_series(
                columns_subset=['Column1', 'Column2'],
                years_subset = None,
                scale_factor=None,
                show_original = True,
                growth_rate = 0.02,
                moving_average_window=3,
                plot_original_moving_average=False,
                plot_scaled_on_original = False,
                plot_growth_rate_moving_average=True,
                plot_growth_rate_on_original=True
            )

        """
        if columns_subset is None:
            columns_subset = self.dataframe.columns

        if years_subset is None:
            years_subset = self.dataframe.index

        num_columns = len(columns_subset)
        num_rows = 1 if num_columns == 1 else num_columns
        # Create subplots
        fig, axs = plt.subplots(
            nrows=num_rows,
            ncols=2,
            figsize=(16, 5 * num_rows),
        )
        # If there's only one column to plot, adjust axes accordingly
        if num_columns == 1:
            axs = axs.reshape(1, -1)

        for i, column in enumerate(columns_subset):
            values = self.dataframe.loc[years_subset, column].values

            # Plot time series on the left plot
            if show_original:
                axs[i, 0].plot(
                    years_subset, values, label=f"Original {column}", linestyle="-"
                )

                # Plot moving average with error bars if specified
                if moving_average_window is not None and plot_original_moving_average:
                    moving_avg = (
                        pd.Series(values)
                        .rolling(window=moving_average_window, min_periods=1)
                        .mean()
                    )
                    axs[i, 0].plot(
                        years_subset,
                        moving_avg,
                        label=f"Original Moving Avg {column}",
                        linestyle="--",
                        alpha=0.7,
                    )

                    # Calculate standard deviation for error bars
                    std_dev = (
                        pd.Series(values)
                        .rolling(window=moving_average_window, min_periods=1)
                        .std()
                    )
                    upper_bound = moving_avg + std_dev
                    lower_bound = moving_avg - std_dev
                    axs[i, 0].fill_between(
                        years_subset,
                        lower_bound,
                        upper_bound,
                        alpha=0.2,
                        label="Original Error Bars",
                    )

                axs[i, 0].set_ylabel("Values")
                axs[i, 0].legend()

            # Apply scaling factor if specified
            if (scale_factor is not None) and (scale_factor != 0.0):
                scaled_values = values * scale_factor

                if plot_scaled_on_original:
                    axs[i, 0].plot(
                        years_subset,
                        scaled_values,
                        label=f"Scaled {column}",
                        linestyle="--",
                        alpha=0.7,
                    )

                axs[i, 0].set_ylabel("Values")
                axs[i, 0].legend()

            # Calculate and plot series with new compound growth rate on the left plot
            if (growth_rate is not None) and (growth_rate != 0.0):
                # Calculate the series under the new compound growth rate
                periods = np.arange(1, len(years_subset) + 1)
                growth_values = values * (1 + growth_rate) ** periods
                # growth_values = values * np.power(1 + growth_rate, periods)

                if plot_growth_rate_on_original:
                    axs[i, 0].plot(
                        years_subset,
                        growth_values,
                        label=f"With Growth Rate {column}",
                        linestyle="--",
                        alpha=0.7,
                    )

                # Plot delta on the right plot
                delta = growth_values - values
                axs[i, 1].bar(
                    years_subset,
                    delta,
                    label=f"Delta (Growth Rate {column})",
                    alpha=0.7,
                )

                axs[i, 1].set_ylabel("Delta")
                axs[i, 1].legend()

                # Plot scaled moving average with error bars if specified
                if (
                    plot_growth_rate_moving_average
                    and moving_average_window is not None
                ):
                    growth_moving_avg = (
                        pd.Series(growth_values)
                        .rolling(window=moving_average_window, min_periods=1)
                        .mean()
                    )
                    axs[i, 0].plot(
                        years_subset,
                        growth_moving_avg,
                        label=f"Growth Moving Avg {column}",
                        linestyle="--",
                        alpha=0.7,
                    )

                    # Calculate standard deviation for error bars
                    scaled_std_dev = (
                        pd.Series(growth_values)
                        .rolling(window=moving_average_window, min_periods=1)
                        .std()
                    )
                    scaled_upper_bound = growth_moving_avg + scaled_std_dev
                    scaled_lower_bound = growth_moving_avg - scaled_std_dev
                    axs[i, 0].fill_between(
                        years_subset,
                        scaled_lower_bound,
                        scaled_upper_bound,
                        alpha=0.2,
                        label="Growth Error Bars",
                    )

            handles, labels = axs[i, 0].get_legend_handles_labels()
            axs[i, 0].legend(handles, labels, loc="best")

        axs[-1, 0].set_xlabel("Year")
        axs[-1, 1].set_xlabel("Year")

        plt.suptitle(f"{self.kind}")

        # Adjust layout to ensure the legend is visible
        plt.tight_layout()

        plt.show()

    def apply_growth_rate(self, series, growth_rate):
        """
        Apply compound growth rate to a time series.

        Parameters:
        - series (pd.Series): Time series data to apply the growth rate to.
        - growth_rate (float): Compound growth rate.

        Returns:
        - pd.Series: Time series with applied growth rate.
        """
        periods = len(series)
        index = series.index
        adjusted_series = pd.Series(index=index, dtype=float)

        for t in range(periods):
            adjusted_series[index[t]] = series[index[t]] * (1 + growth_rate) ** t

        return adjusted_series

    def plot_multiple_time_series(
        self, columns_subset=None, years_subset=None, growth_rates=None, show_original=True
    ):
        """
        Plot multiple time series on one plot with optional compound growth rates.

        Parameters:
        - columns_subset (list or None): List of column names to be plotted. If None, plot all columns.
        - years_subset (list or None): List of years to be plotted. If None, plot all years.
        - growth_rates (dict or None): Dictionary where keys are column names, and values are growth rates.

        Example:
            ts_plotter = TimeSeriesPlotter(df)
            columns_to_plot = ['Column1', 'Column2']
            years_to_plot = [2010, 2015, 2020]
            growth_rates_dict = {'Column1': 0.05, 'Column2': -0.02}

            ts_plotter.plot_multiple_time_series(
                columns_subset=['Column1', 'Column2'],
                years_subset = None,
                growth_rates = growth_rates_dict
            )
        """
        # If columns_subset is None, plot all columns
        if columns_subset is None:
            columns_subset = self.dataframe.columns.tolist()

        # If years_subset is None, plot all years
        if years_subset is None:
            years_subset = self.dataframe.index.tolist()

        # Check if the provided columns_subset and years_subset are valid
        for column in columns_subset:
            if column not in self.dataframe.columns:
                raise ValueError(f"Column '{column}' not found in the dataframe.")
        for year in years_subset:
            if year not in self.dataframe.index:
                raise ValueError(f"Year '{year}' not found in the dataframe index.")

        # Subset the dataframe based on the provided columns_subset and years_subset
        subset_df = self.dataframe.loc[years_subset, columns_subset]

        # Plot the original time series
        plt.figure(figsize=(10, 6))
        for column in columns_subset:

            if show_original:
                plt.plot(subset_df.index, subset_df[column], label=f"{column} (Original)")

            # Apply growth rate if provided
            if growth_rates and (column in growth_rates):
                adjusted_series = self.apply_growth_rate(
                    subset_df[column], growth_rates[column]
                )
                plt.plot(
                    subset_df.index,
                    adjusted_series,
                    linestyle="--",
                    label=f"{column} (Adjusted)",
                )

        # Set plot labels and title
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.title("Multiple Time Series Plot with Growth Rates")

        # Show legend
        plt.legend()

        # Display the plot
        plt.show()

    def plot_time_series_with_distribution(
        self, column_subset=None, year_subset=None, growth_rate=None
    ):
        """
        Plot time series and their distributions on a plot.

        Parameters:
        - column_subset (list or None): List of column names to be plotted. If None, plot all columns.
        - year_subset (list or None): List of years to be plotted. If None, plot all years.
        - growth_rate (float, optional): Compound growth rate to apply to the values.

        Basic Usage:
            columns_to_plot = ['Column1', 'Column2', 'Column3']
            years_to_plot = None
            growth_rate_to_apply = 0.05

            ts_plotter.plot_time_series_with_distribution(columns_to_plot, years_to_plot, growth_rate_to_apply)
        """
        # If column_subset is None, plot all columns
        if column_subset is None:
            column_subset = self.dataframe.columns.tolist()

        # If year_subset is None, plot all years
        if year_subset is None:
            year_subset = self.dataframe.index.tolist()

        # Check if the provided column_subset and year_subset are valid
        for column in column_subset:
            if column not in self.dataframe.columns:
                raise ValueError(f"Column '{column}' not found in the dataframe.")
        for year in year_subset:
            if year not in self.dataframe.index:
                raise ValueError(f"Year '{year}' not found in the dataframe index.")

        num_columns = len(column_subset)
        num_rows = 1 if num_columns == 1 else num_columns
        # Create subplots
        fig, axes = plt.subplots(
            nrows=num_rows,
            ncols=3,
            figsize=(18, 5 * num_rows),
            gridspec_kw={"width_ratios": [3, 1, 1]},
        )
        # If there's only one column to plot, adjust axes accordingly
        if num_columns == 1:
            axes = axes.reshape(1, -1)

        # Iterate over specified columns
        for i, column_name in enumerate(column_subset):
            # Get the specified time series
            original_series = self.dataframe.loc[year_subset, column_name]
            # Apply growth rate if provided
            if growth_rate is not None:
                adjusted_series = self.apply_growth_rate(original_series, growth_rate)

                # Plot the original time series
                axes[i, 0].plot(
                    original_series.index, original_series, label="Original"
                )
                axes[i, 0].plot(
                    original_series.index, adjusted_series, label="Adjusted"
                )
                axes[i, 0].set_title(f"Time Series Plot - {column_name}")
                axes[i, 0].set_xlabel("Year")
                axes[i, 0].set_ylabel("Value")
                axes[i, 0].legend()

                # Plot the distribution of the original series
                sns.histplot(original_series, kde=True, ax=axes[i, 1])
                axes[i, 1].set_title(f"Original Distribution - {column_name}")
                axes[i, 1].set_xlabel("Value")
                axes[i, 1].set_ylabel("Density")

                # Plot the distribution of the adjusted series
                sns.histplot(adjusted_series, kde=True, ax=axes[i, 2])
                axes[i, 2].set_title(f"Adjusted Distribution - {column_name}")
                axes[i, 2].set_xlabel("Value")
                axes[i, 2].set_ylabel("Density")

                # Set x-axis range for distribution plots
                x_min = min(original_series.min(), adjusted_series.min())
                x_max = max(original_series.max(), adjusted_series.max())
                axes[i, 1].set_xlim(x_min, x_max)
                axes[i, 2].set_xlim(x_min, x_max)

            else:
                # If no growth rate provided, plot only the original time series and its distribution
                # Plot the original time series
                axes[i, 0].plot(
                    original_series.index, original_series, label="Original"
                )
                axes[i, 0].set_title(f"Time Series Plot - {column_name}")
                axes[i, 0].set_xlabel("Year")
                axes[i, 0].set_ylabel("Value")
                axes[i, 0].legend()

                # Plot the distribution of the original series
                sns.histplot(original_series, kde=True, ax=axes[i, 1])
                axes[i, 1].set_title(f"Original Distribution - {column_name}")
                axes[i, 1].set_xlabel("Value")
                axes[i, 1].set_ylabel("Density")

        # Adjust layout
        plt.tight_layout()

        # Display the plot
        plt.show()

    def plot_area_under_curve(
        self, column_subset=None, year_subset=None, growth_rate=None
    ):
        """
        Plot the area under the curve for specified time series.

        Parameters:
        - column_subset (list or None): List of column names to be plotted. If None, plot all columns.
        - year_subset (list or None): List of years to be considered. If None, consider all years.
        - growth_rate (float, optional): Compound growth rate to apply to the values.

        Basic Usage:
            columns_to_plot = ['Column1', 'Column2']
            years_to_plot = None
            growth_rate_to_apply = 0.05

            ts_plotter.plot_area_under_curve(column_subset = columns_to_plot, year_subset = years_to_plot,  growth_rate=growth_rate_to_apply)
        """
        # If column_subset is None, plot all columns
        if column_subset is None:
            column_subset = self.dataframe.columns.tolist()

        # If year_subset is None, consider all years
        if year_subset is None:
            year_subset = self.dataframe.index.tolist()

        # Create subplots
        num_plots = len(column_subset)
        fig, axes = plt.subplots(
            nrows=num_plots, ncols=1, figsize=(10, 6 * num_plots), sharex=True
        )

        # Iterate over specified columns
        for i, column_name in enumerate(column_subset):
            # Get the specified time series
            original_series = self.dataframe.loc[year_subset, column_name]

            # Apply growth rate if provided
            if growth_rate is not None:
                adjusted_series = self.apply_growth_rate(original_series, growth_rate)

                # Plot the original and adjusted time series
                #axes[i].plot(original_series.index, original_series, label="Original")
                axes[i].plot(original_series.index, adjusted_series, label="Adjusted")
                # axes[i].fill_between(original_series.index, original_series, adjusted_series, color='gray', alpha=0.5, label='Area Under Curve')
                axes[i].set_ylabel("Value")
                axes[i].set_title(
                    f"Time Series Plot with Area Under Curve - {column_name}"
                )
                axes[i].legend()

            # If no growth rate provided, plot only the original time series
            axes[i].plot(original_series.index, original_series, label="Original")
            axes[i].fill_between(
                original_series.index,
                0,
                original_series,
                color="gray",
                alpha=0.5,
                label="Area Under Curve",
            )
            axes[i].set_ylabel("Value")
            axes[i].set_title(f"Time Series Plot with Area Under Curve - {column_name}")
            axes[i].legend()

        # Set x-axis label and adjust layout
        plt.xlabel("Year")
        plt.tight_layout()

        # Display the plot
        plt.show()

    def plot_heatmap(self, column_subset=None, year_subset=None, growth_rate=None):
        """
        Create two heatmaps of multiple time series: one for original values and one after growth rate has been applied.

        Parameters:
        - column_subset (list or None): List of column names to be included in the heatmap. If None, include all columns.
        - year_subset (list or None): List of years to be included in the heatmap. If None, include all years.
        - growth_rate (float, optional): Compound growth rate to apply to the values.

        Basic Usage:
            # Specify the columns, years, and growth rate for plotting
            columns_to_plot = None
            years_to_plot = None
            growth_rate_to_apply = 0.05

            # Plot the two heatmaps for the specified time series
            ts_plotter.plot_heatmap(columns_to_plot, years_to_plot, growth_rate_to_apply)
        """
        # If column_subset is None, include all columns
        if column_subset is None:
            column_subset = self.dataframe.columns.tolist()

        # If year_subset is None, include all years
        if year_subset is None:
            year_subset = self.dataframe.index.tolist()

        # Check if the provided column_subset and year_subset are valid
        for column in column_subset:
            if column not in self.dataframe.columns:
                raise ValueError(f"Column '{column}' not found in the dataframe.")
        for year in year_subset:
            if year not in self.dataframe.index:
                raise ValueError(f"Year '{year}' not found in the dataframe index.")

        # Create a subset of the dataframe based on column_subset and year_subset
        subset_df = self.dataframe.loc[year_subset, column_subset]

        # Apply growth rate if provided
        if growth_rate is not None:
            adjusted_df = subset_df.apply(
                lambda series: self.apply_growth_rate(series, growth_rate)
            )

            # Plot two heatmaps side by side
            fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))

            # Heatmap for original values
            sns.heatmap(
                subset_df.T,
                cmap="YlGnBu",
                annot=False,
                fmt=".2f",
                cbar_kws={"label": "Value"},
                ax=axes[0],
            )
            axes[0].set_title("Heatmap of Original Values")
            axes[0].set_xlabel("Year")
            axes[0].set_ylabel("Time Series")

            # Heatmap for values after growth rate has been applied
            sns.heatmap(
                adjusted_df.T,
                cmap="YlGnBu",
                annot=False,
                fmt=".2f",
                cbar_kws={"label": "Value"},
                ax=axes[1],
            )
            axes[1].set_title("Heatmap after Growth Rate Application")
            axes[1].set_xlabel("Year")
            axes[1].set_ylabel("Time Series")

            # Adjust layout
            plt.tight_layout()

            # Display the plot
            plt.show()

        else:
            # If no growth rate provided, plot only the heatmap for original values
            plt.figure(figsize=(12, 8))
            sns.heatmap(
                subset_df.T,
                cmap="YlGnBu",
                annot=False,
                fmt=".2f",
                cbar_kws={"label": "Value"},
            )
            plt.title("Heatmap of Original Values")
            plt.xlabel("Year")
            plt.ylabel("Time Series")
            plt.show()


class TimeSeriesVisualizer:
    """This simply visualizes the data using other methods

    Basic Usage:

        plotter = TimeSeriesVisualizer(df)

        plotter.plot_horizontal_bar_chart(columns=['Column1', 'Column2'], years=None)
        plotter.plot_horizontal_bar_subplots(columns=['Column1', 'Column2'], years=None, growth_rate=0.05)
        plotter.plot_overlapping_bar(columns=['Column1', 'Column2', 'Column3'], years=None)
        plotter.plot_overlapping_stacked_bar(columns=['Column1', 'Column2', 'Column3'], years=None)
        plotter.plot_overlapping_area_lines(columns=['Column1', 'Column2', 'Column3'], years=None)
        plotter.plot_stacked_area_chart(columns=['Column1', 'Column2', 'Column3'], years=None)
        plotter.plot_stacked_ratio_chart(columns=['Column1', 'Column2', 'Column3'], years=None)
    """

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def calculate_growth_values(self, values, growth_rate):
        t = np.arange(len(values))
        growth_values = values * (1 + growth_rate) ** t
        return growth_values

    def plot_horizontal_bar_chart(self, columns=None, years=None):
        if columns is None:
            columns = self.dataframe.columns
        if years is None:
            years = self.dataframe.index

        data_to_plot = self.dataframe.loc[years, columns]
        data_to_plot.plot(kind="barh", stacked=True)
        plt.xlabel("Values")
        plt.ylabel("Time")
        plt.title("Horizontal Bar Chart")
        plt.show()

    def plot_horizontal_bar_subplots(self, columns=None, years=None, growth_rate=None):
        if columns is None:
            columns = self.dataframe.columns
        if years is None:
            years = self.dataframe.index
            
        num_columns = len(columns)
        num_rows = 1 if num_columns == 1 else num_columns
        fig, axes = plt.subplots(
            nrows=num_rows, ncols=1, figsize=(10, 5 * num_rows), squeeze = False
        )

        for i, col in enumerate(columns):
            data_to_plot = self.dataframe.loc[years, col]

            if growth_rate is not None:
                growth_values = self.calculate_growth_values(
                    data_to_plot.values, growth_rate
                )
                axes[i,0].barh(
                    data_to_plot.index,
                    data_to_plot,
                    color="black",
                    label="Original Series",
                )
                axes[i,0].barh(
                    data_to_plot.index,
                    growth_values,
                    color="green",
                    alpha=0.7,
                    label=f"Growth Rate: {growth_rate}",
                )
            else:
                axes[i,0].barh(
                    data_to_plot.index,
                    data_to_plot,
                    color="blue",
                    label="Original Series",
                )

            axes[i,0].set_xlabel("Values")
            axes[i,0].set_ylabel("Time")
            axes[i,0].set_title(f"Horizontal Bar Chart - {col}")
            axes[i,0].legend()

        plt.tight_layout()
        plt.show()

    def plot_overlapping_bar(self, columns=None, years=None):
        if columns is None:
            columns = self.dataframe.columns
        if years is None:
            years = self.dataframe.index

        num_series = len(columns)
        colors = plt.cm.Set1(
            range(num_series)
        )  # Using Set1 color map for distinct colors

        data_to_plot = self.dataframe.loc[years, columns]
        ax = data_to_plot.plot(
            kind="bar", alpha=0.4, color=colors, edgecolor="black", width=0.8
        )  # Set width for complete overlap
        ax.set_xlabel("Time")
        ax.set_ylabel("Values")
        ax.set_title("Overlapping Bar Chart")
        ax.legend(columns)

        plt.show()

    def plot_overlapping_stacked_bar(self, columns=None, years=None):
        if columns is None:
            columns = self.dataframe.columns
        if years is None:
            years = self.dataframe.index

        data_to_plot = self.dataframe.loc[years, columns]
        data_to_plot_percentage = data_to_plot.div(
            data_to_plot.sum(axis=1), axis=0
        )  # Normalize by row to get proportions

        num_series = len(columns)
        colors = plt.cm.Set1(
            range(num_series)
        )  # Using Set1 color map for distinct colors

        ax = data_to_plot_percentage.plot(
            kind="bar",
            stacked=True,
            alpha=0.7,
            color=colors,
            edgecolor="black",
            width=0.8,
        )
        ax.set_xlabel("Time")
        ax.set_ylabel("Proportion of Total")
        ax.set_title("Overlapping Stacked Bar Chart")
        ax.legend(columns)

        plt.show()

    def plot_overlapping_area_lines(self, columns=None, years=None):
        if columns is None:
            columns = self.dataframe.columns
        if years is None:
            years = self.dataframe.index

        data_to_plot = self.dataframe.loc[years, columns]
        colors = plt.cm.Set1(range(len(columns)))
        fig, ax = plt.subplots(1, 1, figsize=(18, 6))

        for i, col in enumerate(columns):
            y_values = data_to_plot[col].values
            ax.plot(data_to_plot.index, y_values, color=colors[i], label=col)
            ax.fill_between(data_to_plot.index, 0, y_values, color=colors[i], alpha=0.4)

        ax.set_xlabel("Time")
        ax.set_ylabel("Values")
        ax.set_title("Overlapping Area Line Chart")
        ax.legend()

        plt.show()

    def plot_stacked_area_chart(self, columns=None, years=None):
        if columns is None:
            columns = self.dataframe.columns
        if years is None:
            years = self.dataframe.index

        data_to_plot = self.dataframe.loc[years, columns]
        colors = plt.cm.Set1(range(len(columns)))
        fig, ax = plt.subplots(1, 1, figsize=(18, 6))

        stacked_data = data_to_plot.cumsum(axis=1)

        for i, col in enumerate(columns):
            if i == 0:
                ax.fill_between(
                    data_to_plot.index,
                    0,
                    stacked_data[col],
                    color=colors[i],
                    alpha=0.4,
                    label=col,
                )
            else:
                ax.fill_between(
                    data_to_plot.index,
                    stacked_data[columns[i - 1]],
                    stacked_data[col],
                    color=colors[i],
                    alpha=0.4,
                    label=col,
                )

        ax.set_xlabel("Time")
        ax.set_ylabel("Values")
        ax.set_title("Stacked Area Chart")
        ax.legend()

        plt.show()

    def plot_stacked_ratio_chart(self, columns=None, years=None):
        if columns is None:
            columns = self.dataframe.columns
        if years is None:
            years = self.dataframe.index

        data_to_plot = self.dataframe.loc[years, columns]
        colors = plt.cm.Set1(range(len(columns)))
        fig, ax = plt.subplots(1, 1, figsize=(18, 6))

        total = data_to_plot.sum(axis=1)
        stacked_data = data_to_plot.div(total, axis=0).cumsum(axis=1)

        for i, col in enumerate(columns):
            if i == 0:
                ax.fill_between(
                    data_to_plot.index,
                    0,
                    stacked_data[col],
                    color=colors[i],
                    alpha=0.4,
                    label=col,
                )
            else:
                ax.fill_between(
                    data_to_plot.index,
                    stacked_data[columns[i - 1]],
                    stacked_data[col],
                    color=colors[i],
                    alpha=0.4,
                    label=col,
                )

        ax.set_xlabel("Time")
        ax.set_ylabel("Ratio")
        ax.set_title("Multiple Stacked Ratio Chart")
        ax.legend()

        plt.show()


class SubPlot3DPlotter:
    """Plots Multiple timeseries 3d on subplots

    Basic Usage:
        from data_generators import data_for_3d

        df = data_for_3d(num_years = 50, num_cols = 5)
        plotter = SubPlot3DPlotter(df)
        plotter.plot_3d_line(subset_columns=['Column1', 'Column2'], subset_years=None)
    """

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def plot_3d_line(self, subset_columns=None, subset_years=None):
        # Apply optional subsets
        df = self.dataframe.copy()
        if subset_columns is not None:
            df = df[subset_columns]

        if subset_years is not None:
            df = df[df.index.isin(subset_years)]

        # Create subplots
        fig = plt.figure(figsize=(12, 8))
        fig.suptitle("Interactive 3D Subplots of Time Series")

        for i, column in enumerate(df.columns, 1):
            ax = fig.add_subplot(len(df.columns), 1, i, projection="3d")
            times = df.index
            values = df[column]
            line = ax.plot(range(len(times)), [1] * len(df), values, label=column)

            ax.set_xlabel("Time")
            ax.set_xticks(range(len(times)))
            ax.set_xticklabels([str(time) for time in times], rotation=45)
            ax.set_yticks([1])
            ax.set_yticklabels([column])
            ax.set_zlabel("Value")
            ax.set_title(column)

            # Use mplcursors for interactive data labels
            mplcursors.cursor(line, hover=True).connect(
                "add",
                lambda sel: sel.annotation.set_text(f"{column}: {sel.target[2]:.2f}"),
            )

        # Adjust layout
        fig.tight_layout(rect=[0, 0, 1, 0.96])

        # Show plot
        plt.show()


class SubplotDonutPlotter:
    """Plot Donut Plots showing proportions

    Basic Usage:
        # Assuming df1 and df2 are your DataFrames
        dataframes = [df, df1, df2]

        subplot_donut_plotter = SubplotDonutPlotter()
        # Specify a subset of years (e.g., [2020, 2021]) or leave it as None to include all years
        subset_years = [2020, 2021,2023,2024]
        # Choose aggregation type: 'column' or 'year'
        aggregation_type = 'column'
        subplot_donut_plotter.plot_multi_dataframe_donuts(dataframes, aggregation_type, subset_years)
        subplot_donut_plotter.plot_donut_subplots_by_column(df, subset_years)
        subplot_donut_plotter.plot_donut_subplots_by_year(df, subset_years)
    """

    def plot_donut_subplots_by_column(self, dataframe, subset_years=None):
        if subset_years is not None:
            df_subset = dataframe.loc[subset_years]
        else:
            df_subset = dataframe
        num_plots = len(df_subset.columns)
        cols = int(np.ceil(np.sqrt(num_plots)))
        rows = int(np.ceil(num_plots / cols))

        fig, axes = plt.subplots(rows, cols, figsize=(15, 15))

        for i, column in enumerate(df_subset.columns):
            ax = axes.flatten()[i] if num_plots > 1 else axes
            values = df_subset[column].values
            labels = df_subset.index
            ax.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops=dict(width=0.3),
            )
            ax.axis(
                "equal"
            )  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title(f"Donut Plot - {column}")

        plt.tight_layout()
        plt.show()

    def plot_donut_subplots_by_year(self, dataframe, subset_years=None):
        if subset_years is not None:
            df_subset = dataframe.loc[subset_years]
        else:
            df_subset = dataframe
        num_plots = len(df_subset.index)
        cols = int(np.ceil(np.sqrt(num_plots)))
        rows = int(np.ceil(num_plots / cols))

        fig, axes = plt.subplots(rows, cols, figsize=(15, 15))

        for i, year in enumerate(df_subset.index.tolist()):
            ax = axes.flatten()[i] if num_plots > 1 else axes
            values = dataframe.T[year].values
            labels = dataframe.T.index

            ax.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops=dict(width=0.3),
            )
            ax.axis(
                "equal"
            )  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title(f"Donut Plot - {year}")

        plt.tight_layout()
        plt.show()

    def plot_multi_dataframe_donuts(
        self, dataframes, aggregation_type="column", subset_years=None
    ):
        num_plots = len(dataframes)
        cols = int(np.ceil(np.sqrt(num_plots)))
        rows = int(np.ceil(num_plots / cols))

        fig, axes = plt.subplots(
            rows, cols, figsize=(15, 15), gridspec_kw={"hspace": 0.4}
        )

        for i, df in enumerate(dataframes):
            row = i // cols
            col = i % cols
            ax = axes[row, col] if num_plots > 1 else axes
            if aggregation_type == "column":
                self.plot_column_aggregated_donut(ax, df, subset_years)
            elif aggregation_type == "year":
                self.plot_aggregated_donut(ax, df, subset_years)
            ax.set_title(f"Donut Plot - DataFrame {i+1}")

        if (num_plots % 2) != 0:
            # Delete the last subplot
            fig.delaxes(axes[rows - 1, cols - 1])

        # plt.tight_layout()
        plt.show()

    def plot_column_aggregated_donut(self, ax, df, subset_years=None):
        if subset_years is not None:
            df_subset = df.loc[subset_years]
        else:
            df_subset = df

        total_per_column = df_subset.sum(axis=0)
        labels = total_per_column.index

        ax.pie(
            total_per_column.values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops=dict(width=0.3),
        )
        ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    def plot_aggregated_donut(self, ax, df, subset_years=None):
        if subset_years is not None:
            df_subset = df.loc[subset_years]
        else:
            df_subset = df

        total_cost_per_year = df_subset.sum(axis=1)
        labels = total_cost_per_year.index

        ax.pie(
            total_cost_per_year.values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops=dict(width=0.3),
        )
        ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.


if __name__ == "__main__":

    print("Hello")
