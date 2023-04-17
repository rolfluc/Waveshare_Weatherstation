import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

fig = plt.figure()

ax1 = fig.add_subplot(211)
ax1.set_title('Large Plot')

xdata = [1 ,2 ,3 ,4 ,5]
ydata = [1 ,2 ,3 ,4 ,5]
labels = ['A', 'B', 'C', 'D', 'E']

for i in range(len(xdata)):
    ax1.text(xdata[i], ydata[i]+0.2, labels[i], color='green')
    
ax1.plot(xdata,ydata,'bo-', color='blue') # plot line in blue
ax1.scatter(xdata,ydata,color='black') # plot points in black

# Fill area between line and y=2
ax1.fill_between([xdata[0], xdata[1]], [ydata[0], ydata[1]], 3, facecolor='gray', alpha=0.5)

# Add lines outlining gray shaded box
ax1.plot([xdata[0], xdata[0]], [ydata[0], 3],'k-') # vertical line at x=xdata[0]
ax1.plot([xdata[1], xdata[1]], [ydata[1], 3],'k-') # vertical line at x=xdata[1]

# Create image
image = np.zeros((40,40,3))
image[:,:,0] = 255 # set red channel to max value

# Add image
imagebox = OffsetImage(image,zoom=.2)
ab = AnnotationBbox(imagebox,(np.mean([xdata[0], xdata[1]]),(max(ydata)-min(ydata))*((np.mean([ydata[0], ydata[1]])-min(ydata))/(max(ydata)-min(ydata)))+min(ydata)),frameon=False)
ax1.add_artist(ab)

ax2 = fig.add_subplot(223)
ax2.set_title('Small Plot 1')
ax2.tick_params(labelsize=12) # set axis label font size to 12
ax2.title.set_fontsize(14) # set title font size to 14

ax3 = fig.add_subplot(224)
ax3.set_title('Small Plot 2')
ax3.tick_params(labelsize=12) # set axis label font size to 12
ax3.title.set_fontsize(26) # set title font size to 14

plt.subplots_adjust(hspace=0.5)

# Save figure
dpi = 100 # set desired dpi (dots per inch)
width_px,height_px=(600,400) # set desired figure size in pixels (width,height)
fig.set_size_inches(width_px/dpi,height_px/dpi) # convert pixel dimensions to inches and set figure size accordingly
fig.savefig('figure.png', dpi=dpi) # save figure as png with specified dpi

plt.show()