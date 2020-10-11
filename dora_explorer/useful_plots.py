
class HTMLPlotter(object):
	def __init__(self):
		pass


	def do_map_line_plot(self, go, lats, lons, width):
		"""
		Draw the map plot joining the line between two locations
		:param go: plotly object
		:param list lats: List of latitudes
		:param list lons: List of longitudes
		:param (int, float) width: line width
		:return: plotly object
		"""
		chunk = go.Scattermapbox(
			mode='lines',
			lat=lats,
			lon=lons,
			line=dict(
				width=width
			),
			text='',
			hoverinfo='text'
		)
		return chunk


	def do_map_marker_plot(self, go, lats, lons, size, text_list, color='#78159a'):
		"""
		Draw the map plot (scrtter plot) of locations (marker)
		:param go: plotly object
		:param list lats: List of latitudes
		:param list lons: List of longitudes
		:param (int, float) size: Size of the marker
		:param list text_list: List of places
		:param string color: Color of the marker ('#78159a')
		:return: plotly object
		"""
		chunk = go.Scattermapbox(
			mode='markers',
			lat=lats,
			lon=lons,
			marker=go.scattermapbox.Marker(
				size=size,
				color=color,
			),
			text=text_list,
			hoverinfo='text'
		)
		return chunk


	def do_map_layout(self, go, title, accesstoken, center_lat, center_lon, zoom, style):
		"""
		Design the layout of the plot
		:param go: plotly object
		:param string title: Title of the plot
		:param string accesstoken: Mapbox API key
		:param float center_lat:
		:param float center_lon:
		:param any(int, float) zoom:
		:param string style: Style of the map plot
		:return: plotly object
		"""
		chunk_layout = go.Layout(
			title=title,
			autosize=True,
			height=600,
			hovermode='closest',
			showlegend=False,
			mapbox=dict(
				accesstoken=accesstoken,
				bearing=0,
				center=dict(
					lat=center_lat,
					lon=center_lon
				),
				pitch=0,
				zoom=zoom,
				style=style
			),
			margin=dict(l=40, r=40, t=40, b=40)
		)
		return chunk_layout


	def do_marker_scatter(self, go, x, y, size, color='#78159a'):
		"""
		Draw the normal scatter plot with markers
		:param go: plotly object
		:param list x: List of values
		:param list y: List of values
		:param (int, float) size: Size of the marker
		:param string color: Color of the marker ('#78159a')
		:return: plotly object
		"""
		chunk = go.Scatter(
			x=x,
			y=y,
			mode='markers',
			marker=dict(
				size=size,
				color=color
			)
		)
		return chunk


	def do_line_scatter(self, go, x, y, width):
		"""
		Draw the normal scatter plot with lines
		:param go: plotly object
		:param list x: List of values
		:param list y: List of values
		:param (int, float) width: Width of the line
		:return: plotly object
		"""
		chunk = go.Scatter(
			x=x,
			y=y,
			mode='lines',
			line=dict(
				width=width
			)
		)
		return chunk

	
	def do_scatter_layout(self, go, title):
		"""
		Design the layout - scatter plot
		:param go: plotly object
		:param string title: Title of the plot
		"""
		chunk_layout = go.Layout(
			title=title,
			margin=dict(l=40, r=40, t=40, b=40)
		)
		return chunk_layout