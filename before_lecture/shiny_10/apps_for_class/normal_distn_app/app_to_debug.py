from shiny import App, render, ui
from shinywidgets import render_altair, output_widget

app_ui = ui.page_fluid(
    ui.panel_title("Histogram of 200 Draws from Normal with mean mu"),
    ui.input_slider("mu", "mean mu", 0, 100, 20)
    output_widget("my_hist")
)

def server(input, output, session):
    @render_altair
    def my_hist():
        sample = np.random.normal(input.mu(), 20, 100)
        df = pd.DataFrame({'sample': sample})
        return(
            alt.Chart(df).mark_bar().encode(
                alt.X('sample:Q', bin=True), 
                alt.Y("count()")
            )
        )

app = App(app_ui, server)
