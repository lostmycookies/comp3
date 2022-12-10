#!/usr/bin/env python
# coding: utf-8

# # Nutrition Dashboard
# 
# ## Joseph Cantwell, Adam Davidson, Olive Grace Oliveros, Marlene Perez, Benjamin Polzin
# 
# ### Overview
# 
# This is a proposal for the Computational Methods III course which will use methods learned in class such as Cloud Computing and the use of a git repository to obtain data and create a Dash dashboard then hosting it on AWS.
# 
# ### What is the problem?
# 
# An unbalanced nutritional profile amongst the majority of the world’s population is an increasing problem causing a myriad of health-related concerns and increased risk of disease. Due to the ever-growing demand of “quick and easy” foods, which inherently are composed of highly processed, caloric dense, sugar-ladened ingredients and unhealthy fats, it becomes increasingly difficult for an individual to make healthier food choices in daily life. Especially in the military where mission is first, health and fitness sometimes becomes unprioritized in order to successfully complete a mission. Combined with a busy schedule, lack of healthier food options, and perhaps misleading nutritional information available, fueling the body with proper nutrients to meet the military’s rigorous demands becomes a daunting task and often gets overlooked, thus leading to increased multitude of health-related risks.
# 
# ### Why is it important?
# 
# A healthy diet is an important component to maintain and improve overall health. It helps to protect against health-related risk factors including diabetes, heart disease, stroke and cancer. Additionally, it can be an important element in the treatment of specific conditions like hypertension, obesity, and auto-immune disorders. Helping people making informed decisions about their nutrition and adjusting it to their specific needs is essential to keep current and future generations healthy across the lifespan.
# 
# ### What are we doing to solve this problem?
# 
# Using cloud computing and git as learned in this course, we will develop a "Nutritional Dashboard” which will give the user easy access to nutrition related information in order to increase awareness of the composition of their food intake.
# 
# ### How will you know you have succeeded?
# 
# We will have succeeded when we have a working interactive dashboard with an intuitive interface that provides the user with aggregated information about common foods, including calorie and macro counts.

# ## General Setup:

# In[ ]:


import re
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.express as px
import matplotlib.patches as patches
import matplotlib.pyplot as plt


# In[ ]:


# Read in the data:

base_df = pd.read_csv("nutrients_csvfile.csv")

# Transform the numeric columns into the right format:

cols = base_df.columns.drop(['Food','Category'])
base_df[cols] = base_df[cols].apply(pd.to_numeric, errors='coerce')

# Fill the NA's with 0's for now (THIS IS WRONG, NEED TO DO IT differently later on!!!!)
base_df[cols] = base_df[cols].fillna(0)


# ## Macronutrients Composition

# In[ ]:


#make new DF that groups by Category to then make bar graphs

#prep data
df = base_df[['Calories', 'Category', 'Fat', 'Protein', 'Carbs', 'Fiber']].groupby('Category').apply(lambda x:x.mean())
df.sort_values('Calories', inplace = True)
df.reset_index(inplace=True)

# Introduce breaks for category:

#df['Category'] = df['Category'].map(lambda a : re.sub(",| ,","<br>",a))

#Fix the amount of decimals shown 
df= df.round(decimals=2)


# In[ ]:


# Initialize a figure with ff.create_table(table_data)
colorscale = [[0, '#4d004c'],[.5, '#f2e5ff'],[1, '#ffffff']]
fig = ff.create_table(df, height_constant=60,colorscale=colorscale)

for i in range(len(fig.layout.annotations)):
    fig.layout.annotations[i].font.size = 10
    
#Make traces 
fiber = go.Bar(x = df.Category, y=df.Fiber, 
                 marker = dict(color = '#000000'), #ffc1fe
                 name ='Fiber',
                 xaxis = 'x2', yaxis = 'y2')

fats = go.Bar(x = df.Category,y= df.Fat, 
                 marker = dict(color = '#4f009a'),
                 name ='Fat',
                 xaxis = 'x2', yaxis = 'y2')
protein = go.Bar(x = df.Category, y=df.Protein, 
                 marker = dict(color = '#9a0098'),
                 name ='Protein',
                 xaxis = 'x2', yaxis = 'y2')
carbs = go.Bar(x = df.Category, y=df.Carbs, 
                 marker = dict(color = '#ff7775'),
                 name ='Carbs',
                 xaxis = 'x2', yaxis = 'y2')

#add traces to figure 
fig.add_traces([fats, protein, carbs, fiber])

#intialize xaxis2 and yaxis2
fig['layout']['xaxis2'] = {}
fig['layout']['yaxis2'] = {}

# Edit layout for subplots
fig.layout.xaxis.update({'domain': [0, .5]})
fig.layout.xaxis2.update({'domain': [0.6, 1.]})

# The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
fig.layout.yaxis2.update({'anchor': 'x2'})

fig.layout.yaxis2.update({'title': 'Average Grams'})

# Update the margins to add a title and see graph x-labels.
fig.layout.margin.update({'t':40, 'b':0})
fig.layout.update({'title': 'Grams per Category'})

fig.update_layout(barmode='stack')

macrofig = fig


# ## Carbs and Calories per 100g

# In[ ]:


# Load the dataset
nutrients = pd.read_excel('nutrients.xlsx')

# Carbohydrates:

fig = px.bar(x = nutrients.Food[0:5], y = nutrients.Carbs[0:5])

fig.update_layout(
    title="Carbs per 100 grams",
    xaxis_title="Food Name",
    yaxis_title="Number of Carbs per 100 grams"
    )

carb_fig = fig
carb_statement = ('The total combined carbs for the selected foods is %.2f carbs.' %sum(nutrients.Carbs[0:5]))

# Calories:

fig = px.bar(x = nutrients.Food[0:5], y = nutrients.Calories[0:5])

fig.update_layout(
    title="Calories per 100 grams",
    xaxis_title="Food Name",
    yaxis_title="Total Calories per 100 grams"
    )

calorie_fig = fig
calorie_statement = ('The total combined calories for all selected foods is %.2f calories.' %sum(nutrients.Calories[0:5]))


# ## Scatterplot about saturated fats

# In[ ]:


# Load the dataset
df = pd.read_csv(r'nutrients_csvfile(cleaned).csv')
df['Category'] = df['Category'].astype(str)
df['Food'] = df['Food'].astype(str)
dropdown_columns = ['Protein','Fiber','Sat.Fat','Carbs']

# Generate structure for graph generation:
food_dict = {}

for categories in df.Category.unique():
    temp_list = []
    for items in df.Food[df.Category == categories].unique():
        temp_list.append(items)
    food_dict[categories] = temp_list
    
names = list(food_dict.keys())
nestedOptions = food_dict[names[0]]

# Graph generation:

fig = px.scatter(
            df,
            x="Calories",
            y="Fat",
            size="Sat.Fat",
            color="Category",
            hover_name="Food",
            log_x=True,
            size_max=60,
)

sat_fig = fig


# ## Build the Dashboard:

# In[ ]:


# General Layout:

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2('Nutrition Dashboard'),
    html.Div(children=[    
        html.Blockquote('Find out more about food on our nutrition dashboard. You can discover interesting facts if you explore the tabs.'),
        dcc.Tabs(id="nutrition-selection", value='nutrition-selection', children=[
            dcc.Tab(label='Macronutrient Composition', value='food-1'),
            dcc.Tab(label='Saturated Fats in Different Foods', value='food-2'),
            dcc.Tab(label='Carbohydrates and Calories per 100g', id='carb_tab', value='food-3'),
            dcc.Tab(label='The Project', value='food-4'),
    ]),
    html.Div(id='food-output'), # place where tabs will be displayed
    ])
])


# In[ ]:


# Callbacks:

@app.callback(Output('food-output', 'children'), Input('nutrition-selection', 'value'))

def tab_creation(tab):
    if tab == 'food-1':
        return html.Div([
            html.H4('Macronutrient Composition'),
            html.H5('Learn more about the macronutrient composition of different types of foods. You can activate and deactivate the categories by clicking on the entries in the legend.'),
            dcc.Graph(id="Macro_Comp_Pic", figure = macrofig),
        ])
    
    if tab == 'food-2':
        return html.Div([
            html.H4('Saturated Fats in Different Foods'),
            html.H5('Learn more about how many saturated fats are in different types of food. You can activate and deactivate the categories by clicking on the entries in the legend.'),
            html.Div([
                dcc.Dropdown(dropdown_columns, id="Scatterdrop", multi=False),
                dcc.Graph(id="Scatter_Pic", figure = sat_fig),
            ]), 
        ])
    
    if tab == 'food-3':
        return html.Div([
            html.H4('Carbohydrates and Calories per 100g'),
            html.H5('Learn more about how much carbohydrates and calories are in different types of food.'),
            html.Div([
                dcc.Dropdown(nutrients.Food, id="Multidrop", multi=True),
                dcc.Graph(id="Carb_100_Pic", figure = carb_fig),
                dcc.Graph(id="Calorie_100_Pic", figure = calorie_fig),
            ]), 
        ])
    
    if tab == 'food-4':
        return html.Div([
            html.H4('Overview'),
            html.H6('This is a proposal for the Computational Methods III course which will use methods learned in class such as Cloud Computing and the use of a git repository to obtain data and create a Dash dashboard then hosting it on AWS.'),
            html.H4('What is the problem?'),
            html.H6('An unbalanced nutritional profile amongst the majority of the world’s population is an increasing problem causing a myriad of health-related concerns and increased risk of disease. Due to the ever-growing demand of “quick and easy” foods, which inherently are composed of highly processed, caloric dense, sugar-ladened ingredients and unhealthy fats, it becomes increasingly difficult for an individual to make healthier food choices in daily life. Especially in the military where mission is first, health and fitness sometimes becomes unprioritized in order to successfully complete a mission. Combined with a busy schedule, lack of healthier food options, and perhaps misleading nutritional information available, fueling the body with proper nutrients to meet the military’s rigorous demands becomes a daunting task and often gets overlooked, thus leading to increased multitude of health-related risks.'),
            html.H4('Why is it important?'),
            html.H6('A healthy diet is an important component to maintain and improve overall health. It helps to protect against health-related risk factors including diabetes, heart disease, stroke and cancer. Additionally, it can be an important element in the treatment of specific conditions like hypertension, obesity, and auto-immune disorders. Helping people making informed decisions about their nutrition and adjusting it to their specific needs is essential to keep current and future generations healthy across the lifespan.'),
            html.H4('What are we doing to solve this problem?'),
            html.H6('Using cloud computing and git as learned in this course, we will develop a "Nutritional Dashboard” which will give the user easy access to nutrition related information in order to increase awareness of the composition of their food intake.'),
            html.H4('How will you know you have succeeded?'),
            html.H6('We will have succeeded when we have a working interactive dashboard with an intuitive interface that provides the user with aggregated information about common foods, including calorie and macro counts.'),
        ])
    
@app.callback(Output('Carb_100_Pic', 'figure'), [Input('Multidrop', 'value')])

def update_carb_picture(values):
    
    # Carbohydrates:
    new_df = nutrients[(nutrients['Food'].isin(values))]
    
    fig_update = px.bar(x = new_df.Food, y = new_df.Carbs)

    fig_update.update_layout(
        title="Carbs per 100 grams",
        xaxis_title="Food Name",
        yaxis_title="Number of Carbs per 100 grams"
        )
    
    return fig_update

@app.callback(Output('Calorie_100_Pic', 'figure'), [Input('Multidrop', 'value')])

def update_calorie_picture(values):
    
    # Calories:
    new_df = nutrients[(nutrients['Food'].isin(values))]
    
    fig_update = px.bar(x = new_df.Food, y = new_df.Calories)

    fig_update.update_layout(
        title="Calories per 100 grams",
        xaxis_title="Food Name",
        yaxis_title="Number of calories per per 100 grams"
        )
    
    return fig_update
    
@app.callback(Output('Scatter_Pic', 'figure'), [Input('Scatterdrop', 'value')])

def update_calorie_picture(values):
    
    fig_scat = px.scatter(
            df,
            x="Calories",
            y="Fat",
            size=values,
            color="Category",
            hover_name="Food",
            log_x=True,
            size_max=60,
    )
    
    return fig_scat


# ## Run the Server locally:

# In[ ]:


# Run the App:

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)

