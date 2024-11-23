from shiny import App, render, ui, reactive
import pandas as pd 
import matplotlib.pyplot as plt

app_ui = ui.page_fluid(
    ui.input_select(id = 'state', label = 'Choose a state:',
    choices = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]),
    ui.input_switch("anotherstate", "Two States", False),
    ui.input_radio_buttons(id = 'outcome', label = 'Choose an outcome:', choices = ["Cases", "Deaths"]),
    ui.panel_conditional(
        "!input.anotherstate",
        ui.output_plot("ts"),
        ui.input_checkbox("show", "Show Data")
    ),
    ui.panel_conditional(
         "!input.anotherstate && input.show",
         ui.output_table("subsetted_data_table")
    ),
    ui.panel_conditional(
        "input.anotherstate", 
        ui.input_select(id = 'state2', label = 'Choose a state:',
        choices = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]),
        ui.output_plot("ts2")
    )
    
)


def server(input, output, session):
    @reactive.calc
    def full_data():
        return pd.read_csv("covid-conditional-advanced/nyt covid19 data.csv", parse_dates = ['date'])

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

    @render.plot
    def ts2():
        df = subsetted_data2()
        state1_data = df[df['state'] == input.state()]
        state2_data = df[df['state'] == input.state2()]
        if input.outcome() == "Cases":
            series1 = state1_data['cases']
            series2 = state2_data['cases']
        if input.outcome() == "Deaths":
            series1 = state1_data['deaths']
            series2 = state2_data['deaths']
        fig, ax = plt.subplots(figsize=(3,6))
        ax.plot(state1_data['date'], series1, label = input.state())
        ax.plot(state2_data['date'], series2, label = input.state2())
        ax.legend()
        ax.tick_params(axis = 'x', rotation = 45)
        ax.set_xlabel('Date')
        ax.set_ylabel(input.outcome())
        ax.set_title(f'COVID-19 {input.outcome()} in {input.state()} and {input.state2()}')
        ax.set_yticklabels(['{:,}'.format(int(x)) for x in ax.get_yticks()])
        return fig
    
    
    
app = App(app_ui, server)
