import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as table
from dash.dependencies import (Input, Output)
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.offline import plot_mpl

from flask import Flask
import os
import json, random
from pandas import DataFrame
from collections import OrderedDict

from travel_places import GeoTraveller
from india_data import india_dumped

external_stylesheets = [
	'https://codepen.io/chriddyp/pen/bWLwgP.css'
]

with open('mapbox_token.txt', 'r') as mr:
	mapbox_access = mr.read()

server = Flask(__name__)
server.secret_key = os.environ.get('secret_key', 'rickyman9')

app = dash.Dash(
	__name__,
	external_stylesheets=external_stylesheets,
	server=server
)

all_cities = list(india_dumped.keys())
df = DataFrame(OrderedDict([
    ('cities', ['Bengaluru', 'Mumbai', 'Delhi', 'Cochin']),
]))

app.layout = html.Div([
	html.Div([
		html.Div([
			table.DataTable(
				id='table-dropdown',
				data=df.to_dict('records'),
					columns=[
						{'id': 'cities', 'name': '', 'presentation': 'dropdown'},
					],
					editable=True,
					dropdown={
						'cities' : {
							'options': [
								{'label': i, 'value': i} for i in all_cities
							]
						},
					}
				),
		], className='two columns',
			style={
				'padding-left' : 20,
				'padding-top' : 40,
				'padding-bottom' : 20
			}
		),
		html.Div([
			html.Div([
				dcc.RadioItems(
					id='norm-direction',
					options=[
						{'label' : 'Normal', 'value' : 'normal'},
						{'label' : 'Directions', 'value' : 'directions'}
					],
					value='normal',
					labelStyle={
						'display' : 'inline-block', 
						'padding-left' : 20
					}
				)
			], style={'padding-top' : 30, 'padding-left' : 30}),
			html.Div([
				dcc.Graph(
					id='better-travel',
					config={'toImageButtonOptions' : {'width' : None, 'height' : None}}
				)
			], style={'text-align' : 'center', 'padding' : 20})
		], className='ten columns')
	], className='row', style={})
])

@app.callback(
	Output(component_id='better-travel', component_property='figure'),
	[Input(component_id='norm-direction', component_property='value'),
		Input(component_id='table-dropdown', component_property='data')]
)
def get_least_distance(option_type, data):
	lats = [india_dumped[i['cities']][0] for i in data]
	lons = [india_dumped[i['cities']][1] for i in data]
	place_names = [str(i['cities']) for i in data]

	place_list = {i : j for (i, j) in zip([1, 2, 3, 4], place_names)}
	place_coords = {i : j for (i, j) in zip(
		place_names, [india_dumped[c] for c in place_names]
	)}

	center_lat = sum(lats) / len(lats)
	center_lon = sum(lons) / len(lons)

	geo_travel = GeoTraveller(
		place_list=place_list,
		place_coords=place_coords,
		geo_token=mapbox_access
	)

	place_path, dis = geo_travel.get_place_path()
	order_places = geo_travel.order_places
	order_path = geo_travel.order_path
	place_names = list(place_coords.keys())

	data = []
	for each_join in range(len(order_path)):
		from_, to_ = order_path[each_join]
		if option_type == 'normal':
			lats_, lons_ = geo_travel.get_coords_joining(from_=from_, to_=to_)
		elif option_type == 'directions':
			lats_, lons_ = geo_travel.get_travel_route(from_=from_, to_=to_)
		else:
			lats_ = []; lons_ = []

		data.append(
			go.Scattermapbox(
			mode='lines',
			lat=lats_,
			lon=lons_,
			line=dict(
				width=2.5,
				# color='#2ead83'
			),
			text='',
			hoverinfo='text'
			)
		)

	data.append(
		go.Scattermapbox(
			mode='markers',
			lat=lats,
			lon=lons,
			marker=go.scattermapbox.Marker(
				size=15,
				color='#78159a',
				# opacity=0.7
			),
			text=place_names,
			hoverinfo='text'
		)
	)

	layout = go.Layout(
		title='Dora the Geo - Explorer',
		autosize=True,
		height=600,
		hovermode='closest',
		showlegend=False,
		mapbox=dict(
			accesstoken=mapbox_access,
			bearing=0,
			center=dict(
				lat=center_lat,
				lon=center_lon
			),
			pitch=0,
			zoom=3.5,
			style='outdoors'
		),
		margin=dict(l=40, r=40, t=40, b=40)
	)

	result = {'data' : data, 'layout' : layout}
	# plot_mpl(result)
	# plot_mpl(result, image='png')

	return result






# if __name__ == '__main__':
# 	app.run_server(debug=True)