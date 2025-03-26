import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px



def bubble_chart_plot(classroom_id=None, assignment_name=None, month_index=7):


    MONTH_MAP = {
        0: 'Aug',  # August
        1: 'Sep',  # September
        2: 'Oct',  # October
        3: 'Nov',  # November
        4: 'Dec',  # December
        5: 'Jan',  # January
        6: 'Feb',  # February
        7: 'Mar',   # March
        8: 'Apr',  # April
        9: 'May',  # May
        10: 'Jun',  # June
        11: 'Jul'  # July

    }

    # TODO modify this part to read from the csv with the correct classroom_id
    df_assignments = pd.read_csv('/Users/Gabriela/Desktop/github/website_dashboards/backend/plotly_plots/fake_assignments.csv')

    # Apply classroom filter if classroom_id is provided
    if classroom_id and 'classroom_id' in df_assignments.columns:
        df_assignments = df_assignments[df_assignments['classroom_id'] == int(classroom_id)]

    # Apply assignment filter
    if assignment_name and assignment_name != 'Select Assignment':
        df_assignments = df_assignments[df_assignments['assignment_name'] == assignment_name]

    # Apply month range filter if month_index is provided
    if month_index is not None and 'month' in df_assignments.columns:
        # Get all months from August to the selected month
        selected_months = [MONTH_MAP[i] for i in range(0, month_index + 1)]
        df_assignments = df_assignments[df_assignments['month'].isin(selected_months)]

    df_plot = df_assignments.groupby(['student_id']).agg(
        completion_rate=('completion_rate', 'mean'), #????
        avg_grade=('grade', 'mean'),
        avg_time = ('avg_time_spent', 'mean')
    ).reset_index()

    # Add customdata to include avg_time for hover info
    fig = go.Figure(
        data=[go.Scatter(
        x=df_plot['completion_rate'].to_list(),
        y=df_plot['avg_grade'].to_list(),
        mode='markers',
        marker=dict(
            color=df_plot['student_id'].to_list(),  # set as an string
            size=list(df_plot['avg_time']/10),
            colorscale=px.colors.qualitative.Set1,  # Discrete color scale
            showscale=False  # Hide the color scale legend
        )
        ,
        text=df_plot['avg_grade'].apply(lambda x: f"{x:.2f}"),  # Add text as grade
        customdata=df_plot['avg_time'].apply(lambda x: f"{x:.2f} seconds")  # Add avg_time as custom data
    )])
    # Add hover information
    fig.update_traces(
        hovertemplate=(
            'Student ID: %{marker.color}<br>' +
            'Grade: %{text}<br>' +
            'Completed: %{x:.2%}<br>' +
            'Time spent: %{customdata}<br>' +  # Use customdata for time info
            '<extra></extra>'
        )
    )

    # Update the layout to fix the x and y axis ranges
    fig.update_layout(
        xaxis=dict(range=[0, 1.1]),
        yaxis=dict(range=[0, 100])
    )
    return fig