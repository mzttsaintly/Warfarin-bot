from io import BytesIO
from PIL import Image as IMG
from PIL import ImageFont, ImageDraw
import os
import math
import asyncio


async def message_to_img(
    message,
    max_width: int = 1080,
    font_size: int = 40,
    spacing: int = 15,
    padding_x: int = 20,
    padding_y: int = 15,
    img_fixed: bool = True,
    font_path: str = os.path.join(os.getcwd(), "warfarin", "plugins", "Luckpick", "resource", "font.ttc")
):
    ''' Args:
            message: 要转换的文字
            max_width: 最大长度
            font_size: 字体尺寸
            spacing: 行间距
            padding_x: x轴距离边框大小
            padding_y: y轴距离边框大小
            img_fixed: 图片是否适应大小（仅适用于图片小于最大长度时）
            font_path: 字体文件路径
        Examples:
            msg = await messagechain_to_img(message=message)
    '''
    def get_final_text_lines(text: str, text_width: int, font: ImageFont.FreeTypeFont) -> int:
            lines = text.split("\n")
            line_count = 0
            for line in lines:
                if not line:
                    line_count += 1
                    continue
                line_count += int(math.ceil(float(font.getsize(line)[0]) / float(text_width)))
            return line_count + 1

    font = ImageFont.truetype(font_path, font_size, encoding="utf-8")
    plains = message
    final_width = min(max(font.getsize(text)[0] for text in plains.split("\n")) + 2 * padding_x, max_width)
    text_width = final_width - 2 * padding_x
    text_height = (font_size + spacing) * (get_final_text_lines(plains, text_width, font) + 1)

    final_height = 2 * padding_y + text_height
    picture = IMG.new('RGB', (final_width, final_height), (255, 255, 255))
    draw = ImageDraw.Draw(picture)
    present_x = padding_x
    persent_y =padding_y
    draw.text((padding_x, padding_y), plains, font=font, fill=(0,0,0))
    bytes_io = BytesIO()
    picture.save(bytes_io, format="PNG")
    



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(message_to_img("test image maker"))
#     text = "test image maker"
#     im = Image.new("RGB", (300, 50), (255, 255, 255))
#     dr = ImageDraw.Draw(im)
#     font = ImageFont.truetype((os.path.dirname(__file__) + "/resource/font.ttc"), 18)
#     dr.text((10, 5), text,font=font, fill="#000000")
#     im.show()
    # im.save(os.path.dirname(__file__) + "/resource/out_put.png")