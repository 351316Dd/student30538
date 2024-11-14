from shiny import App, render, ui
import matplotlib.pyplot as plt
import numpy as np

app_ui = ui.page_fluid(
    ui.panel_title("Histogram of 200 Draws from Normal with mean mu"),
    ui.input_slider("mu", "mean mu", 0, 100, 20), 
    ui.output_plot("my_hist")
)

def server(input, output, session):
    @render.plot
    def my_hist():
        sample = np.random.normal(input.mu(), 20, 200)
        fig, ax = plt.subplots()
        ax.hist(sample, bins=30, color='blue', alpha=0.7)
        return fig

app = App(app_ui, server)
