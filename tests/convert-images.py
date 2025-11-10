import base64
import os

with open(r"C:\Project\InventarioSanRafael\tests\test-images\laptop.jpg", "rb") as image_file:
    base64_string = base64.b64encode(image_file.read()).decode('utf-8')