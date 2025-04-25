from htmlnode import HTMLNode

class LeafNode(HTMLNode):

	def __init__(self, tag, value, props=None):  # Default props to an empty dictionary
		if value is None:
			raise ValueError('All leaf nodes must have a value.')
		if props is None:  # Ensure props is at least an empty dictionary
			props = {}
		super().__init__(tag, value, props)
	
	def to_html(self):
		# Prepare props string if any props exist
		props_str = " ".join(f'{key}="{value}"' for key, value in self.props.items()) if self.props else ""

		# Render based on whether a tag is present
		if self.tag:
			# Include props if available
			if props_str:
				return f'<{self.tag} {props_str}>{self.value}</{self.tag}>'
			else:
				return f'<{self.tag}>{self.value}</{self.tag}>'
		else:
			return self.value  # No tag means return raw value