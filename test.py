from PIL import Image, ImageDraw, ImageFont

# Load the "Times New Roman" font
font = ImageFont.truetype("times.ttf", 24)

# Create a new image with white background
img = Image.new('RGB', (600, 448), 'white')
d = ImageDraw.Draw(img)

# Create a separate bitmap for the red square
square_size = 40
square_img = Image.new('RGB', (square_size, square_size), 'red')

# Define the rectangles and their labels
rectangles = [(100, 50, 500, 198), (75, 250, 275, 398), (325, 250, 525, 398)]
labels = ["Graph 1", "Graph 2", "Graph 3"]

for i, rect in enumerate(rectangles):
    # Draw a black outline
    d.rectangle(rect, outline='black')

    # Draw ticks along the bottom
    x1, y1, x2, y2 = rect
    tick_spacing = (x2 - x1) / 8
    for j in range(8):
        x = x1 + j * tick_spacing
        d.line([(x, y2), (x, y2 + 10)], fill='black')

        # Draw the number below the tick
        d.text((x, y2 + 15), str(j+1), fill='black', anchor='ms', font=font)

    # Draw the label above the rectangle
    label_x = x1 + (x2 - x1) / 2
    label_y = y1 - 10
    d.text((label_x, label_y), labels[i], fill='black', anchor='ms', font=font)

    # Paste the red square bitmap into the center of the top rectangle
    if i == 0:
        square_x = int(x1 + (x2 - x1) / 2 - square_size / 2)
        square_y = int(y1 + (y2 - y1) / 2 - square_size / 2)
        img.paste(square_img, (square_x, square_y))

        # Draw a line from halfway to 2/3 on the y-axis, between the 2nd and 3rd tick on the x-axis
        line_y1 = y1 + (y2 - y1) / 2
        line_y2 = y1 + (y2 - y1) * 2 / 3
        line_x1 = line_x2 = x1 + tick_spacing * 2
        d.line([(line_x1, line_y1), (line_x2, line_y2)], fill='black')

        # Draw a blue polygon with 6 points above the line
        polygon_points = [(x1, y1), (x2, y1), (x2, line_y1), (line_x1, line_y1), (line_x1, y1), (x1, y1)]
        d.polygon(polygon_points, fill='blue')

# Display the image
img.show()