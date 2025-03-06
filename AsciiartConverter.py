import sys
import argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ASCII character set for contrast, ordered from darkest(@) to lightest( )
ASCII_CHARS = "@%#*+=-:. "

# Grayscale conversion using perceptual model
def grayscale_value(r, g, b):
    """
    Converts RGB to grayscale using a perceptual model
    In simple way how much human eye is sensitive to different colors
    """
    return int(0.299 * r + 0.587 * g + 0.114 * b)  # Weighted average for human vision

def convertImageToAscii(fileName, cols, scale):
    """
    Converts an image to ASCII chars
    """
    image = Image.open(fileName).convert("RGB")  # Ensure RGB mode
    image = image.resize((cols, int(cols * image.size[1] / image.size[0])))
    W, H = image.size

    w = W / cols
    h = w / scale
    rows = int(H / h)
        
    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))

    #Checking if Image is Large Enough
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    aimg = []   # Initializing the ASCII image list
    # Loop through the image by row
    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)
        if j == rows - 1:
            y2 = H
        
        #Initialization of a New ASCII Row
        aimg.append("")
        
        # Loop through each column
        for i in range(cols):
            x1 = int(i * w)
            x2 = int((i + 1) * w)
            if i == cols - 1:
                x2 = W

            img = image.crop((x1, y1, x2, y2))
            pixels = np.array(img)
            avg_gray = np.mean([grayscale_value(r, g, b) for r, g, b in pixels.reshape(-1, 3)])
            gsval = ASCII_CHARS[int((avg_gray / 255) * (len(ASCII_CHARS) - 1))]  # Map to ASCII range
            aimg[j] += gsval

    return aimg

def saveAsciiAsImage(aimg, outFile):
    """
    saves ASCII image as an actual image file
    """
    font_size = 10
    img_width = len(aimg[0]) * font_size
    img_height = len(aimg) * font_size
    img = Image.new('RGB', (img_width, img_height), 'white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    for i, row in enumerate(aimg):
        for j, char in enumerate(row):
            color = (0, 0, 0) if char != ' ' else (255, 255, 255)  # Black text, white space
            draw.text((j * font_size, i * font_size), char, fill=color, font=font)

    img.save(outFile, 'JPEG')

def main():
    parser = argparse.ArgumentParser(description="This program converts an image into ASCII art.")
    parser.add_argument('--file', dest='imgFile', required=True) # Input image file
    parser.add_argument('--scale', dest='scale', type=float, default=1) # Scaling factor
    parser.add_argument('--out', dest='outFile', default='out.jpg') # Output file name
    parser.add_argument('--cols', dest='cols', type=int, default=100) # Number of columns
    args = parser.parse_args()

    print('Generating ASCII art...')
    aimg = convertImageToAscii(args.imgFile, args.cols, args.scale)
    saveAsciiAsImage(aimg, args.outFile)
    print("Converted ASCII art written to", args.outFile)

if __name__ == '__main__':
    main()
