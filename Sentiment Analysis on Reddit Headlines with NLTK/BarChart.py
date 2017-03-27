import matplotlib.pyplot as plt
import numpy as np

# For the bar-chart distribution
y_val = [448/982*100, 307/982*100, 227/982*100]
x_val = [1, 2, 3]
plt.style.use('ggplot')

ind = np.arange(len(x_val))
width = 0.3
fig, ax = plt.subplots()
ax.bar(ind+0.1, y_val,width, color='green')
ax.set_xticks(ind+0.1+width/2)
ax.set_xticklabels(['Neutral', 'Negative', 'Positive'])
ax.legend()
plt.title("Categories Distribution")
plt.xlabel("Categories")
plt.ylabel("Percentage")
