import os
from flask import Flask, render_template, request
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from plotly_plots import teacher_plots
from dash.dependencies import Input, Output
from urllib.parse import urlparse, parse_qs


app = Flask(__name__)

MONTHS = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
MONTH_MAP = {i: month for i, month in enumerate(MONTHS)}

def get_dropdown_options():
    df = pd.read_csv('static/data/df_classrooms_product_week.csv')  # Replace with your CSV filename
    return df

@app.route('/')
def home():
    image_folder = os.path.join(app.static_folder, 'images')
    images = [img for img in os.listdir(image_folder) if img.startswith("formula")]
    return render_template('index.html', images=images, main_image="badger.png")

@app.route('/myclasses')
def myclasses():
    options = get_dropdown_options()
    return render_template('my_classes.html', options=options.to_dict('records'))

@app.route('/dashboard_page', methods=['GET'])
def dashboard_page():
    classroom_id = request.args.get('classroom_id')
    return render_template('main.html', classroom_id=classroom_id)

# Create Dash app
dash_app = dash.Dash(
    __name__,
    server=app,
    url_base_pathname='/dashboard/',
)


# Layout
dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([  # Main container
        # Left panel (original content)
        html.Div([
            # First Row: Dropdown
            html.Div([
                dcc.Dropdown(
                    id='assignment-dropdown',
                    options=[],
                    value='Select Assignment',
                    style={'width': '100%', 'margin-bottom': '20px'}
                )
            ]),
            
            # Graph
            html.Div([
                dcc.Graph(
                    id='main-graph',
                    figure=teacher_plots.bubble_chart_plot(),
                    style={'height': '500px'}
                )
            ], style={'margin-bottom': '20px'}),
            
            # Slider
            html.Div([
                dcc.Slider(
                    id='crossfilter-month-slider',
                    min=0, max=11, value=7,
                    step=None,
                    marks={i: month for i, month in enumerate(MONTHS)},
                    included=True
                )
            ])
        ], style={
            'width': '68%',
            'display': 'inline-block',
            'vertical-align': 'top',
            'padding': '20px',
            'border': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'border-radius': '5px',
            'float': 'left'
        }),
        
       # Right panel with toggle system
        html.Div([
            # Toggle buttons row
            html.Div([
                html.Div([
                    html.Div("View:", style={
                        'display': 'inline-block',
                        'margin-right': '10px',
                        'font-weight': 'bold'
                    }),
                    dcc.RadioItems(
                        id='view-toggle',
                        options=[
                            {'label': 'Top', 'value': 'top'},
                            {'label': 'Lowest', 'value': 'lowest'}
                        ],
                        value='top',
                        labelStyle={'display': 'inline-block', 'margin-right': '15px'},
                        style={'display': 'inline-block'}
                    )
                ], style={'margin-bottom': '20px'}),
                
                html.Div([
                    html.Div("Category:", style={
                        'display': 'inline-block',
                        'margin-right': '10px',
                        'font-weight': 'bold'
                    }),
                    dcc.RadioItems(
                        id='category-toggle',
                        options=[
                            {'label': 'Graded', 'value': 'graded'},
                            {'label': 'Turned In', 'value': 'turned-in'}
                        ],
                        value='graded',
                        labelStyle={'display': 'inline-block', 'margin-right': '15px'},
                        style={'display': 'inline-block'}
                    )
                ])
            ], style={
                'margin-bottom': '20px',
                'padding': '10px',
                'background': '#f5f5f5',
                'border-radius': '5px'
            }),
            
            # Dynamic assignments section
            html.Div(id='assignments-container', children=[
                # This will be populated by the callback
            ])
        ], style={
            'width': '30%',
            'display': 'inline-block',
            'vertical-align': 'top',
            'padding': '20px',
            'margin-left': '2%',
            'border': 'thin lightgrey solid',
            'backgroundColor': 'rgb(240, 240, 240)',
            'border-radius': '5px',
            'float': 'right',
            'overflow-y': 'auto',
            'max-height': '800px'
        })
    ], style={
        'width': '100%',
        'display': 'flex',
        'flex-wrap': 'nowrap'
    })
])

# Add callback to handle the toggle switches
@dash_app.callback(
    Output('assignments-container', 'children'),
    [Input('view-toggle', 'value'),
     Input('category-toggle', 'value')]
)
def update_assignments_view(view_type, category):
    title = f"{view_type.capitalize()} {category.capitalize().replace('-', ' ')}"
    color_map = {
        'top-graded': '#4CAF50',
        'lowest-graded': '#F44336',
        'top-turned-in': '#4CAF50',
        'lowest-turned-in': '#F44336'
    }
    color = color_map.get(f"{view_type}-{category}", '#4CAF50')
    
    return html.Div([
        html.H1(title, style={
            'text-align': 'center',
            'margin-bottom': '15px',
            'font-size': '24px',
            'color': color,
            'font-family': '"GT-Presura-Bold", sans-serif'
        }),
        *[html.Button(
            f'Assignment {i}',
            id=f'{view_type}-{category}-{i}',
            style={
                'width': '100%',
                'height': '50px',
                'margin-bottom': '10px',
                'font-size': '16px',
                'background-color': color,
                'color': 'white',
                'border': 'none',
                'border-radius': '8px',
                'cursor': 'pointer',
                'border-top': '1px solid white'
            }
        ) for i in range(1, 7)]
    ])

    
def load_assignments(classroom_id):
    df = pd.read_csv('/Users/Gabriela/Desktop/github/website_dashboards/backend/plotly_plots/fake_assignments.csv')
    # Filter by classroom_id if your CSV has this column
    if 'classroom_id' in df.columns:
        df = df[df['classroom_id'] == int(classroom_id)]
    return df['assignment_name'].unique()

@dash_app.callback(
    Output('assignment-dropdown', 'options'),
    Input('url', 'href')
)
def update_assignments(href):
    print("Callback triggered!")  # Debug print
    if not href:
        return []
    
    try:
        # Parse the URL properly
        parsed = urlparse(href)
        params = parse_qs(parsed.query)
        classroom_id = params.get('classroom_id', [None])[0]
        
        if classroom_id:
            print(f"Loading assignments for classroom {classroom_id}")
            assignments = load_assignments(classroom_id)
            return [{'label': name, 'value': name} for name in assignments]
    except Exception as e:
        print(f"Error parsing URL: {e}")
    
    return []

@dash_app.callback(
    Output('main-graph', 'figure'),
    [Input('assignment-dropdown', 'value'),
     Input('crossfilter-month-slider', 'value'),  # Add month slider input
     Input('url', 'href')]
)
def update_graph(selected_assignment, selected_month, href):
    # Get classroom_id from URL
    classroom_id = None
    if href:
        try:
            parsed = urlparse(href)
            params = parse_qs(parsed.query)
            classroom_id = params.get('classroom_id', [None])[0]
        except:
            pass
    
    return teacher_plots.bubble_chart_plot(
        classroom_id=classroom_id,
        assignment_name=selected_assignment,
        month_index=selected_month  # Pass the month index to your function
    )
if __name__ == '__main__':
    app.run(debug=True)
