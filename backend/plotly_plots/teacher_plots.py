import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px




# def bubble_chart_plot():
#     # Sample Data
#     fig = go.Figure(data=[go.Scatter(
#         x=[1, 3.2, 5.4, 7.6, 9.8, 12.5],
#         y=[1, 3.2, 5.4, 7.6, 9.8, 12.5],
#         mode='markers',
#         marker=dict(
#             color=[120, 125, 130, 135, 140, 145],
#             size=[15, 30, 55, 70, 90, 110],
#             showscale=True
#         )
#     )])
#     return fig

def bubble_chart_plot():
    df_assignments = pd.read_csv('/Users/adrianrodriguezsanjurjo/Documents/repos/product-week/website_dashboards/backend/plotly_plots/fake_assignments.csv')

    df_plot = df_assignments.groupby(['student_id']).agg(
        completion_rate=('completion_rate', 'mean'),
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