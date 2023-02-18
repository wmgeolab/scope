import torch
import transformers
import os
import json

from ts.torch_handler.base_handler import BaseHandler
from transformers import PegasusForConditionalGeneration, PegasusTokenizer


class PegasusHandler(BaseHandler):
    def initialize(self, context):
        return super().initialize(context)

    def preprocess(self, data):
        return super().preprocess(data)

    def inference(self, data, *args, **kwargs):
        return super().inference(data, *args, **kwargs)

    def postprocess(self, data):
        return super().postprocess(data)
