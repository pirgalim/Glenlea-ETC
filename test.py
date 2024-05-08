import base64
from io import BytesIO
from matplotlib.figure import Figure


def run():
    
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1,2])
    buf = BytesIO()
    fig.savefig(buf, format="png")
    
    
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data