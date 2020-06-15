
class HTMLPlotter(object):
	def __init__(self):
		pass


	def do_map_line_plot(self, go, lats, lons, width):
		"""
		Draw the map plot joining the line between two locations
		:param go: plotly object
		:param lats: list[float]
		:param lons: list[float]
		:param width: any(int, float)
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
		:param lats: list[float]
		:param lons: list[float]
		:param size: any(int, float)
		:param text_list: list[string]
		:param (default) color: string='#78159a'
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


	def do_map_layout(self, go, title, accesstoken, center_lat, center_lon, style):
		"""
		Design the layout of the plot
		:param go: plotly object
		:param title: string
		:param accesstoken: string
		:param center_lat: float
		:param center_lon: float
		:param style: string
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
				zoom=3.5,
				style=style
			),
			margin=dict(l=40, r=40, t=40, b=40)
		)
		return chunk_layout


	def do_marker_scatter(self, go, x, y, size, color='#78159a'):
		"""
		Draw the normal scatter plot with markers
		:param go: plotly object
		:param x: list[any(int, float)],
		:param y: list[any(int, float)],
		:param size: any(int, float),
		:param color: string='#78159a'
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
		:param x: list[any(int, float)],
		:param y: list[any(int, float)],
		:param width: any(int, float)
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
		:param title: string
		"""
		chunk_layout = go.Layout(
			title=title,
			margin=dict(l=40, r=40, t=40, b=40)
		)
		return chunk_layout