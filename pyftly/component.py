class Component:
    def __init__(self, **kwargs):
        self.props = kwargs

    def render(self):
        raise NotImplementedError("Subclasses must implement render() method")
