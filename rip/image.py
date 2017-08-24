# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Factor for antialiasing
factor = 5
# Padding for the images
pad = 5


def make_image(text, fontsize=45, output_file='tmp.png', fontname='HamletOrNot.ttf'):
    """Make an image out of a poem"""
    # Get font
    font = ImageFont.truetype(fontname, fontsize * factor)
    # Compute height
    num_lines = (1 + text.strip().count('\n'))
    height = num_lines * font.getsize(text[:10])[1] / factor + 2 * pad
    # Compute width
    font_length = max(font.getsize(line)[0] for line in text.split('\n'))
    width = font_length / factor + 2 * pad
    # Create big image and draw text
    image = Image.new("RGBA", (width * factor, height * factor), (241, 241, 212))
    draw = ImageDraw.Draw(image)
    draw.text((pad * factor, pad * factor), text, (0, 0, 0), font=font)
    # Resize with antialiasing
    img_resized = image.resize((width, height), Image.ANTIALIAS)
    # Save to file
    img_resized.save(output_file)


def test():
    quatrain = ['Chinese are not good at geography....',
                'This would be an amazing flower pot.',
                'It\'s an apostrophe catastrophe!',
                'It matters not, for matter we are not.']
    make_image('\n'.join(quatrain))


if __name__ == '__main__':
    test()
