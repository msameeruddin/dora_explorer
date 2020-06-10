import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import (Input, Output)
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from travel_places import GeoTraveller

external_stylesheets = [
	'https://codepen.io/chriddyp/pen/bWLwgP.css'
]

with open('mapbox_token.txt', 'r') as mr:
	mapbox_access = mr.read()

app = dash.Dash(
	__name__,
	external_stylesheets=external_stylesheets,
)

place_list = {
	1 : 'Red Fort', 
	2 : 'Pink City', 
	3 : 'Goa', 
	4 : 'Howrah Bridge'
}

place_coords = {
	'Red Fort' : [28.6562, 77.2410],
	'Pink City' : [26.9124, 75.7873],
	'Goa' : [15.2993, 74.1240],
	'Howrah Bridge' : [22.5851, 88.3468]
}

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
				'margin-left' : 20
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
				color='rgb(255, 0, 0)',
				opacity=0.7
			),
			text=place_names,
			hoverinfo='text'
		)
	)

	layout = go.Layout(
		title='Geo - Explorer',
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






if __name__ == '__main__':
	app.run_server(debug=True)