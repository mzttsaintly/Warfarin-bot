from PIL import Image, ImageFont, ImageDraw
import os

if __name__ == "__main__":
    text = "test image maker"
    im = Image.new("RGB", (300, 50), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype((os.path.dirname(__file__) + "/resource/font.ttc"), 18)
    dr.text((10, 5), text,font=font, fill="#000000")
    im.show()
    # im.save(os.path.dirname(__file__) + "/resource/out_put.png")