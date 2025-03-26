import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px



def bubble_chart_plot(classroom_id=None, assignment_name=None, month_index=3):


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
    #/Users/adrianrodriguezsanjurjo/Documents/repos/product-week/website_dashboards/backend/static/data/pw_data_1.csv
    df_assignments = pd.read_csv('/Users/Gabriela/Desktop/github/website_dashboards/backend/static/data/cooked_data.csv')
    # df_assignments = pd.read_csv('/Users/adrianrodriguezsanjurjo/Documents/repos/product-week/website_dashboards/backend/plotly_plots/fake_assignments.csv')
    df_assignments['assignment_due_date'] = pd.to_datetime(df_assignments['assignment_due_date'])
    df_assignments['month_index'] = (df_assignments['assignment_due_date'].dt.month -8) % 12
    
    df_assignments['month'] = df_assignments['month_index'].map(MONTH_MAP)

    # Apply classroom filter if classroom_id is provided
    if classroom_id and 'classroom_id' in df_assignments.columns:
        df_assignments = df_assignments[df_assignments['classroom_id'] == classroom_id]

        # Apply assignment filter
        if assignment_name and assignment_name != 'Select Assignment':
            df_assignments = df_assignments[df_assignments['assignment_title'] == assignment_name]

        # Apply month range filter if month_index is provided
        if month_index is not None and 'month' in df_assignments.columns:
            # Get all months from August to the selected month
            selected_months = [MONTH_MAP[i] for i in range(0, month_index + 1)]
            df_assignments = df_assignments[df_assignments['month'].isin(selected_months)]

    #df_assignments['completed'] = df_assignments['assignment_turned_in_date'].isna()
    df_plot = df_assignments.groupby(['student_user_id']).agg(
        num_assignments=('assignment_id', 'nunique'),
        num_completed=('turned_in_date', 'count'),
        avg_grade=('analytics_grade', 'mean'),
        avg_grade_filtered=('analytics_grade_filtered', 'mean'),
        avg_time=('time_spent', 'mean')
    )

    # Compute the proportion of completed assignments
    df_plot['proportion_completed'] = df_plot['num_completed'] / df_plot['num_assignments']
    # Add customdata to include avg_time for hover info
    fig = go.Figure(
        data=[go.Scatter(
        x=df_plot['proportion_completed'].to_list(),
        y=df_plot['avg_grade_filtered'].to_list(),
        mode='markers',
        marker=dict(
            #color=df_plot['student_user_id'].to_list(),  # set as an string
            size=list(df_plot['avg_time']/360),
            colorscale=px.colors.qualitative.Set1,  # Discrete color scale
            showscale=False  # Hide the color scale legend
        )
        ,
        text=df_plot['avg_grade'].apply(lambda x: f"{x:.2f}"),  # Add text as grade
        customdata=df_plot['avg_time'].apply(lambda x: f"{x:.2f} seconds")  # Add avg_time as custom data
    )])

    print(classroom_id)
    print(assignment_name)
    print(df_plot['avg_grade_filtered'])

    # Add hover information
    fig.update_traces(
        hovertemplate=(
            #'Student ID: %{marker.color}<br>' +
            'Grade: %{text}<br>' +
            'Completed: %{x:.2%}<br>' +
            'Time spent: %{customdata}<br>' +  # Use customdata for time info
            '<extra></extra>'
        )
    )

    # Update the layout to fix the x and y axis ranges
    fig.update_layout(
        xaxis=dict(title='Completed Assignments (%)', range=[-0.01, 1.1]),
        yaxis=dict(title= 'Grade', range=[0, 101])
    )
    return fig