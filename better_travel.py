import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import (Input, Output)
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from flask import Flask
import os
import json, random

from travel_places import GeoTraveller

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

def get_unique_places():
	# with open('indian_cities_geoloc.json', 'r', encoding='utf-8') as ico:
	# 	cities_ = json.load(ico)
	from india_data import india_dumped

	city_names = []
	names_list = list(india_dumped.keys())
	high = len(names_list)
	random.seed(25)
	for i in range(high):
		if len(city_names) >= 4:
			break
		else:
			uni_name = names_list[random.randint(a=0, b=high)]
			if uni_name not in city_names:
				city_names.append(uni_name)

	place_list = {i : j for (i, j) in zip([1, 2, 3, 4], city_names)}
	place_coords = {i : j for (i, j) in zip(city_names, [india_dumped[c] for c in city_names])}

	return place_list, place_coords


place_list, place_coords = get_unique_places()
# print(place_list)
# print(place_coords)

app.layout = html.Div([
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
		)
	], style={'text-align' : 'center', 'padding' : 20})
])

@app.callback(
	Output(component_id='better-travel', component_property='figure'),
	[Input(component_id='norm-direction', component_property='value')]
)
def get_least_distance(option_type):
	geo_travel = GeoTraveller(
		place_list=place_list,
		place_coords=place_coords,
		geo_token=mapbox_access
	)

	place_path, dis = geo_travel.get_place_path()
	order_places = geo_travel.order_places
	order_path = geo_travel.order_path
	coords_list = list(place_coords.values())
	lats = [i[0] for i in coords_list]
	lons = [i[1] for i in coords_list]
	place_names = list(place_coords.keys())
	# print(place_path)
	# print(dis)

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
				lat=20.5937,
				lon=78.9629
			),
			pitch=0,
			zoom=4,
			style='outdoors'
		),
		margin=dict(l=40, r=40, t=40, b=40)
	)

	return {'data' : data, 'layout' : layout}






# if __name__ == '__main__':
# 	app.run_server(debug=True)