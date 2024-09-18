import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('ggplot')

def animate(i):
    data = pd.read_csv('data.csv')
    
    # Group by channel name and sum the likes
    grouped_data = data.groupby('channel_name').sum().reset_index()
    
    plt.cla()
    
    for channel in grouped_data['channel_name']:
        channel_data = data[data['channel_name'] == channel]
        plt.plot(channel_data['upload_date'], channel_data['likes'], label=channel)
    
    plt.legend(loc='upper left')
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, interval=1000, cache_frame_data=False)

plt.tight_layout()
plt.show()
