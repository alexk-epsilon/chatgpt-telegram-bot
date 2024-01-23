import io
import os, random, string
import urllib
import urllib.parse
import urllib.request
from typing import Dict
import matplotlib.pyplot as plt
from cairosvg import svg2png
from PIL import Image
from PIL import ImageOps
from .plugin import Plugin, generate_random_string
import sympy
import logging


class LatexConverterPlugin(Plugin):
    """
    A plugin to answer questions using WolframAlpha.
    """

    def get_source_name(self) -> str:
        return "LatexConverter"

    def get_icon(self) -> str:
        return "🖌️"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "transform_latex_to_image",
            "description": "Transform latex formula to an image. Input should be a valid LaTeX expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "from": {"type": "string", "description": "A string in valid LaTeX format"}
                },
                "required": ["from"]
            }
        }]

    async def execute(self, function_name, helper, **kwargs) -> Dict:
        try:
            latex_data = kwargs['from'] 

            if not os.path.exists("uploads/latex"):
                os.makedirs("uploads/latex")

            image_file_path = os.path.join("uploads/latex", f"{generate_random_string(15)}.png")
            logging.info(f"image_file_path:{image_file_path}")
            sympy.preview(latex_data,viewer='file', filename=image_file_path, euler=False)
      
            return {
                'direct_result': {
                    'kind': 'photo',
                    'format': 'path',
                    'value': image_file_path
                }
            }

        except Exception as e:
            logging.info(f"Unable to convert LaTeX: {e}")
            return {'result': f"Unable to convert LaTeX: {e}"}

