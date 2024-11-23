from shiny import App, render, ui, reactive
import pandas as pd 
import matplotlib.pyplot as plt

app_ui = ui.page_fluid(
    ui.input_select(id = 'state', label = 'Choose a state:', choices = []),
    ui.input_radio_buttons(id = 'outcome', label = 'Choose an outcome:', choices = ["Cases", "Deaths"]),
    ui.output_plot("ts"),
    ui.output_table("subsetted_data_table")
)


def server(input, output, session):
    @reactive.calc
    def full_data():
        return pd.read_csv("covid-update-select/nyt covid19 data.csv", parse_dates = ['date'])

    @reactive.calc
    def subsetted_data():
        df = full_data()
        return df[df['state'] == input.state()]
    
    @reactive.calc
    def subsetted_data2():
        df = full_data()
        return df[(df['state'] == input.state()) | (df['state'] == input.state2())]

    @render.table()
    def subsetted_data_table():
        return subsetted_data()

    @render.plot
    def ts():
        df = subsetted_data()
        if input.outcome() == "Cases":
            series = df['cases']
        if input.outcome() == "Deaths":
            series = df['deaths']
        fig, ax = plt.subplots(figsize=(3,6))
        ax.plot(df['date'], series)
        ax.tick_params(axis = 'x', rotation = 45)
        ax.set_xlabel('Date')
        ax.set_ylabel(input.outcome())
        ax.set_title(f'COVID-19 {input.outcome()} in {input.state()}')
        ax.set_yticklabels(['{:,}'.format(int(x)) for x in ax.get_yticks()])
        return fig
    
    @reactive.effect
    def _():
        state_list = full_data()['state'].unique().tolist()
        state_list = sorted(state_list)
        ui.update_select("state", choices=state_list)
    
    
    
app = App(app_ui, server)
