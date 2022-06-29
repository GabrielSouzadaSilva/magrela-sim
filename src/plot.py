import plotly
import plotly.io as pio

class plot:
    def __init__(self) -> None:
        self.y = []
        self.x = []    

    def apend(self, data):
        self.x.append(data['x'])
        self.y.append(data['y'])
        
    def show(self):
        fig = dict({
            "data": [{"type": "line",
                    "x": self.x,
                    "y": self.y
                    }],
            "layout": {"title": {"text": "A teste"}}
        })

        # To display the figure defined by this dict, use the low-level plotly.io.show function

        pio.show(fig)