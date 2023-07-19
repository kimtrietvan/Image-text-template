# from rembg import remove
# from PIL import Image

# input_path = 'input.jpeg'
# output_path = 'output.png'

# input = Image.open(input_path)
# output = remove(input)
# output.save(output_path)


import uvicorn
from fastapi import FastAPI, Request


app = FastAPI()

@app.get('/')
def get(request: Request):
    return request.query_params

if __name__ == '__main__':
    uvicorn.run("test:app", host="0.0.0.0", port=9090)