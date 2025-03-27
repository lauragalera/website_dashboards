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
from dash.dependencies import Input, Output, State, ALL
from chatgpt_prompts import queries
import random



app = Flask(__name__)

PATH_COOKED = '/Users/Gabriela/Desktop/github/website_dashboards/backend/static/data/cooked_data.csv'

MONTHS = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
MONTH_MAP = {i: month for i, month in enumerate(MONTHS)}

student_names_all = [
    "Emma Johnson",
    "Liam Smith",
    "Olivia Williams",
    "Noah Brown",
    "Ava Jones",
    "William Garcia",
    "Sophia Miller",
    "Benjamin Davis",
    "Isabella Rodriguez",
    "Mason Martinez",
    "Charlotte Hernandez",
    "Elijah Lopez",
    "Amelia Gonzalez",
    "James Wilson",
    "Mia Anderson",
    "Alexander Thomas",
    "Harper Taylor",
    "Michael Moore",
    "Evelyn Jackson",
    "Daniel Martin",
    "Abigail Lee",
    "Matthew Perez",
    "Emily Thompson",
    "David White",
    "Elizabeth Harris",
    "Joseph Sanchez",
    "Sofia Clark",
    "Jackson Ramirez",
    "Avery Lewis",
    "Samuel Robinson",
    "Scarlett Walker",
    "Sebastian Young",
    "Victoria Allen",
    "Henry King",
    "Madison Wright",
    "Owen Scott",
    "Luna Torres",
    "Gabriel Nguyen",
    "Chloe Hill",
    "Julian Flores"
]

DICT_CLASSROOM_NAMES = {
    "6317e8272d03a74142fb038a": "Rick Pd 2 Integrated Math 2",
    "6317e827b62b13414a993841": "Rick Pd 9 Integrated Math 2",
}

def get_dropdown_options():
    df = pd.read_csv(PATH_COOKED)

    # 1. Filter to only include classrooms in our dictionary
    valid_ids = list(DICT_CLASSROOM_NAMES.keys())
    filtered_df = df[df['classroom_id'].isin(valid_ids)].copy()
    
    return filtered_df[['classroom_id','classroom_name','classroom_subj_grade']].drop_duplicates()

def get_students_list(classroom_id):
    df = pd.read_csv(PATH_COOKED)

    unique_student_ids = df[df['classroom_id'] == classroom_id]['student_user_id'].unique()
        
    # Convert to list for JSON serialization
    student_list = unique_student_ids.tolist()

    students_names = random.sample(student_names_all, len(student_list))
        
    # Pair IDs with names here in Python
    student_pairs = list(zip(student_list, students_names))

    return student_pairs


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
    classroom_name = DICT_CLASSROOM_NAMES[classroom_id]
    return render_template('main.html', classroom_id=classroom_id, classroom_name=classroom_name)

@app.route('/badger_report')
def badger_report():
    classroom_id = request.args.get('classroom_id')
    
    if not classroom_id:
        print("ERROR: Missing classroom_id parameter")
        return "Error: Classroom ID is required", 400
    
    try:
        message = queries.welcome_message()
        students_pairs = get_students_list(classroom_id)
        
        return render_template(
            'badger_report.html',
            message=message.content,
            classroom_id=classroom_id,
            student_pairs=students_pairs  # Pass the pre-zipped pairs
        )
        
    except Exception as e:
        print(f"Error in badger_report: {str(e)}")
        return "An error occurred", 500

@app.route('/report_student')
def report_student():
    df = pd.read_csv(PATH_COOKED)
    
    classroom_id = request.args.get('classroom_id')
    student_id = request.args.get('student_id')
    student_name = request.args.get('student_name')
        
    # Your report generation logic here
    return render_template('student_report.html',
                         classroom_id=classroom_id,
                         student_id=student_id,
                         student_name=student_name)



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
                html.H1('LEADERBOARD', style={
                    'text-align': 'center',
                    'margin-bottom': '15px',
                    'font-size': '24px',
                    'font-family': '"GT-Presura-Bold", sans-serif'
                }),             
                html.Div([
                    html.Div("Category:", style={
                        'display': 'inline-block',
                        'margin-right': '10px',
                        'font-weight': 'bold',
                        'font-family': '"GT-Presura-Bold", sans-serif'
                    }),
                    dcc.RadioItems(
                        id='category-toggle',
                        options=[
                            {'label': 'Graded', 'value': 'graded'},
                            {'label': 'Turned In', 'value': 'turned-in'}
                        ],
                        value='graded',
                        labelStyle={'display': 'inline-block', 'margin-right': '15px'},
                        style={'display': 'inline-block','font-family': '"GT-Presura-Bold", sans-serif'
}
                    )
                ])
            ], style={
                'margin-bottom': '14px',
                'padding': '10px',
                'background': '#f5f5f5',
                'border-radius': '5px'
            }),          
            html.Div(id='assignments-container', children=[
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

@dash_app.callback(
    Output('assignments-container', 'children'),
    [Input('category-toggle', 'value'),
     Input('url', 'href')]
)
def update_assignments_view(category, href):
    if not href:
        return []
    
    try:
        parsed = urlparse(href)
        params = parse_qs(parsed.query)
        classroom_id = params.get('classroom_id', [None])[0]
        
        if classroom_id:
            top_assignments = load_assignments_ordered(classroom_id, 'top', category)
            lowest_assignments = load_assignments_ordered(classroom_id, 'lowest', category)
            
            print(top_assignments)
            return html.Div([
                # Top Assignments Card
                html.Div([
                    html.H4(f"🏆 TOP {category.upper()}", 
                           style={
                               'color': '#2E7D32',
                               'text-align': 'center',
                               'margin-bottom': '15px',
                               'font-family': '"GT-Presura-Bold", sans-serif',
                               'border-bottom': '2px solid #E0E0E0',
                               'padding-bottom': '8px'
                           }),
                    html.Ul([
                        html.Li(
                            html.Div([
                                html.Span(f"{i+1}. ", style={
                                    'color': '#2E7D32',
                                    'font-weight': 'bold',
                                    'min-width': '30px',
                                    'display': 'inline-block'
                                }),
                                html.Span(assign, style={
                                    'color': '#424242',
                                    'transition': 'all 0.2s ease'
                                })
                            ], style={
                                'padding': '10px 15px',
                                'margin-bottom': '6px',
                                'background': '#FAFAFA',
                                'border-radius': '6px',
                                'border-left': '4px solid #81C784',
                                'box-shadow': '0 1px 3px rgba(0,0,0,0.05)',
                                'display': 'flex',
                                'align-items': 'center',
                                'font-family': '"GT-Presura-Bold", sans-serif',

                            }),
                            style={
                                'list-style-type': 'none',
                                'margin-bottom': '8px',
                                'cursor': 'pointer',
                                ':hover': {
                                    'transform': 'translateX(5px)'
                                }
                            }
                        ) for i, assign in enumerate(top_assignments)
                    ], style={'padding': '0', 'margin': '0'})
                ], style={
                    'background': 'white',
                    'padding': '20px',
                    'border-radius': '10px',
                    'margin-bottom': '25px',
                    'box-shadow': '0 2px 10px rgba(0,0,0,0.08)',
                    'border': '1px solid #EEEEEE'
                }),
                
                # Lowest Assignments Card
                html.Div([
                    html.H4(f"📉 LOWEST {category.upper()}", 
                           style={
                               'color': '#C62828',
                               'text-align': 'center',
                               'margin-bottom': '15px',
                               'font-family': '"GT-Presura-Bold", sans-serif',
                               'border-bottom': '2px solid #E0E0E0',
                               'padding-bottom': '8px',

                           }),
                    html.Ul([
                        html.Li(
                            html.Div([
                                html.Span(f"{i+1}. ", style={
                                    'color': '#C62828',
                                    'font-weight': 'bold',
                                    'min-width': '30px',
                                    'display': 'inline-block'
                                }),
                                html.Span(assign, style={
                                    'color': '#424242'
                                })
                            ], style={
                                'padding': '10px 15px',
                                'margin-bottom': '6px',
                                'background': '#FAFAFA',
                                'border-radius': '6px',
                                'border-left': '4px solid #E57373',
                                'box-shadow': '0 1px 3px rgba(0,0,0,0.05)',
                                'display': 'flex',
                                'align-items': 'center',
                                'font-family': '"GT-Presura-Bold", sans-serif',
                            }),
                            style={
                                'list-style-type': 'none',
                                'margin-bottom': '8px',
                                'cursor': 'pointer',
                                ':hover': {
                                    'transform': 'translateX(5px)'
                                }
                            }
                        ) for i, assign in enumerate(lowest_assignments)
                    ], style={'padding': '0', 'margin': '0'})
                ], style={
                    'background': 'white',
                    'padding': '20px',
                    'border-radius': '10px',
                    'box-shadow': '0 2px 10px rgba(0,0,0,0.08)',
                    'border': '1px solid #EEEEEE'
                })
            ], style={
                'background': '#F5F5F5',
                'padding': '25px',
                'border-radius': '12px',
                'box-shadow': '0 4px 12px rgba(0,0,0,0.1)',
                'border': '1px solid #E0E0E0'
            })
            
    except Exception as e:
        print(f"Error: {e}")
        return []

# Update the load function to handle view_type
def load_assignments_ordered(classroom_id, view_type, category):
    df = pd.read_csv('/Users/Gabriela/Desktop/github/website_dashboards/backend/static/data/cooked_data.csv')
    
    if 'classroom_id' in df.columns:
        df = df[df['classroom_id'] == classroom_id]

    category_select = 'grade' if category == 'graded' else 'completion_rate'
    
    df = df.groupby('assignment_title').agg(
        grade=('analytics_grade_filtered', 'mean'),
        completion_rate=('completed', 'mean')
    ).reset_index()
    
    # Sort based on view type
    if view_type == 'top':
        df = df.nlargest(3, category_select)
    else:
        df = df.nsmallest(3, category_select)
    
    return df['assignment_title'].tolist()


############################# FILTER BY ASSIGNMENT ######################################## 
#  
def load_assignments(classroom_id):
    df = pd.read_csv('/Users/Gabriela/Desktop/github/website_dashboards/backend/static/data/cooked_data.csv')
    # Filter by classroom_id if your CSV has this column
    if 'classroom_id' in df.columns:
        df = df[df['classroom_id'] == classroom_id]
    return df['assignment_title'].unique()

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
            assignments = load_assignments(classroom_id)
            return [{'label': name, 'value': name} for name in assignments]
    except Exception as e:
        print(f"Error parsing URL: {e}")
    
    return []


################################# UPDATE MAIN BUBBLE PLOT ###################################
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
