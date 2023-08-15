from PIL import Image, ImageDraw, ImageFont, ImageColor
import requests
import io
import json
from rembg import remove, new_session
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response
app = FastAPI()

class Template:
    def __init__(self, template):
        path = f'templates/{template}.json'
        self.template = json.load(open(path))
        self.width = self.template['size']['width']
        self.height = self.template['size']['height']
    def calcXY(self, element):
        x = element['position']['x']
        y = element['position']['y']
        width = element['size']['width']
        height = element['size']['height']
        if x == 'center':
            x = (self.width - width) / 2
        if y == 'center':
            y = (self.height - height) / 2

        return x, y
    def calcXYText(self, element, content, font):
        x = element['position']['x']
        y = element['position']['y']
        image = Image.new(mode="RGB", size=(self.width, self.height))
        box = ImageDraw.Draw(image)
        _, _, w, d = box.textbbox((0, 0), content, font=font)
        if x == 'center':
            x = (self.width - w) / 2
        if y == 'center':
            y = (self.height - d) / 2
        return x, y, w, d

    def render(self, kwagrs) -> Image:
        background = None
        if self.template['name'] not in kwagrs:
            raise Exception(f"Missing {self.template['name']}")
        if self.template['type'] == 'image':
            background = Image.open(io.BytesIO(requests.get(kwagrs[self.template['name']]).content))
            print("Hello")
            background = background.resize((self.template['size']['width'], self.template['size']['height']))
        if self.template['type'] == 'solid':
            background = Image.new(mode='RGB', size=(self.template['size']['width'], self.template['size']['height']), color=ImageColor.getrgb(f"#{kwagrs[self.template['name']]}"))
        for element in self.template['elements']:
            if element['name'] not in kwagrs:
                raise Exception(f"Missing {element['name']}")
            # Render text
            if element['type'] == 'text':
                if f'{element["name"]}_color' in kwagrs:
                    element['font']['color'] = kwagrs[f'{element["name"]}_color']
                content: str = kwagrs[element['name']]
                font = ImageFont.truetype(font='fonts/' + element['font']['family'], size=element['font']['size'])
                draw = ImageDraw.Draw(background)
                x, y, w, d = self.calcXYText(element=element, content=content, font=font)
                if w > self.width:
                    contents = content.split(" ")
                    index : int = -1
                    while True:
                        left = " ".join(contents[0:index])
                        x, y, w, d = self.calcXYText(element=element, content=left, font=font)
                        if w > self.width:
                            index -= 1
                        else:
                            right = " ".join(contents[index:])
                            draw.text(xy=(x, y), text=left, font=font, fill=ImageColor.getrgb(element['font']['color']))
                            draw.text(xy=(x, y + d), text=right, font=font, fill=ImageColor.getrgb(element['font']['color']))
                            break
                else:
                    draw.text(xy=(x, y), text=content, font=font, fill=ImageColor.getrgb(element['font']['color']))
            # Render image
            if element['type'] == 'image':
                url = kwagrs[element['name']]
                image = Image.open(io.BytesIO(requests.get(url).content))
                image = image.resize((element['size']['width'], element['size']['height']))
                x, y = self.calcXY(element=element)
                background.paste(image, (x, y))
            # Render image with remove background
            if element['type'] == 'remove-background':
                url = kwagrs[element['name']]
                image = Image.open(io.BytesIO(requests.get(url).content))
                image = image.resize((element['size']['width'], element['size']['height']))
                remove = RemoveBackground('u2net')
                remove.load_session()
                x, y = self.calcXY(element=element)
                image = remove.remove(image=image)
                background.paste(image, (x, y), image)
        return background
                
class RemoveBackground:
    def __init__(self, model: str) -> None:
        self.model = model
    def load_session(self) -> None:
        self.session = new_session(self.model)
    def remove(self, image: Image) -> Image:
        return remove(data=image, session=self.session, alpha_matting=True, post_process_mask=True, alpha_matting_foreground_threshold=270 ,alpha_matting_background_threshold=20, alpha_matting_erode_size=11)
    

    

    

"""
if __name__ == '__main__':
    test = Template('templates/template.json')
    title = 'Logo car'
    product = 'https://joytoyfigure.com/wp-content/uploads/2022/09/Warhammer-40K.jpg'
    logo = "https://cdn.joytoyfigure.com/wp-content/uploads/2023/01/joytoy-figure-New-logo.png"
    background = 'https://www.ledr.com/colours/white.jpg'
    image = test.render(background=background, title=title, logo=logo, product=product)
    image.save('a.png')
"""


@app.get('/image.png')
def get(request: Request):
    # try:
        params = request.query_params
        template = Template(params['template'])
        image = template.render(params)
        imageByte = io.BytesIO()
        image.save(imageByte, format='PNG')
        return Response(imageByte.getvalue())
    # except Exception as e:
    #     return Response(str(e))



if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=80, reload=True)

# def main(url: str, title_text: str | None = '') -> None:
#     background = Image.open(io.BytesIO(requests.get(url=url, stream=True).content))
#     title_size = 1
#     title_font = ImageFont.truetype(font='Montserrat-Black.ttf', size=title_size)
#     draw = ImageDraw.Draw(background)
#     while True:
#         _, _, w, _ = draw.textbbox((0, 0), text=title_text, font=title_font)
#         if w < 0.5 * background.width:
#             title_size += 1
#             title_font = ImageFont.truetype(font='Montserrat-Black.ttf', size=title_size)
#         else: 
#             break
#     draw.text(xy=((background.width - w)/ 2 + 4, 1), text=title_text, font=title_font, fill=ImageColor.getrgb("#9E9E9E"))
#     draw.text(xy=((background.width - w)/ 2, 1), text=title_text, font=title_font, fill=ImageColor.getrgb("#8C0000"))
#     print(f"Text width: {w}")
#     print(f"Height: {background.height}")
#     print(f"Width: {background.width}")
#     background.save('test.png')
# if __name__ == '__main__':
    # main(url='https://img.freepik.com/premium-photo/abstract-rainbow-colorful-bright-feather-closeup-up-macro-view-background-plumage-texture-with-dew-drops_753134-644.jpg', title_text="aaaaaaaaaaaaa")