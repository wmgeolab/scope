import torch
import transformers
import os
import json
import logging

from ts.torch_handler.base_handler import BaseHandler
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

logger = logging.getLogger(__name__)
logger.info("Transformers version %s", transformers.__version__)


class PegasusHandler(BaseHandler):
    def __init__(self):
        self.initialized = False

    def initialize(self, context):
        properties = context.system_properties
        self.manifest = context.manifest
        model_dir = properties.get("model_dir")

        # Use GPU if available
        self.device = torch.device(
            "cuda:" + str(properties.get("gpu_id"))
            if torch.cuda.is_available() and properties.get("gpu_id") is not None
            else "cpu"
        )

        logger.info(f"Using device {self.device}")

        # Load model
        model_file = self.manifest["model"]["modelFile"]
        model_path = os.path.join(model_dir, model_file)

        if os.path.isfile(model_path):
            self.model = PegasusForConditionalGeneration.from_pretrained(model_dir)
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"Successfully loaded model from {model_file}")
        else:
            raise RuntimeError(f"Model file not found. Path: {model_path}")

        # Load tokenizer
        self.tokenizer = PegasusTokenizer.from_pretrained(model_dir)
        if self.tokenizer is not None:
            logger.info(f"Successfully loaded tokenizer")
        else:
            raise RuntimeError("Missing tokenizer")

        self.initialied = True

    def preprocess(self, text):
        # Unpack Data
        logger.info(f"Text Received: {text}")
        logger.info(f"Received {len(text)} texts. Begin tokenizing")

        # Tokenize Texts
        tokenized_data = self.tokenizer(
            text,
            truncation=True,
            padding="longest",
            return_tensors="pt",
        )

        logger.info("Tokenization process completed")

        return tokenized_data

    def inference(self, inputs):
        translated = self.model.generate(**inputs)
        output = self.tokenizer.batch_decode(translated, skip_special_tokens=True)

        logger.info(f"Summary successfully generated")

        return output

    def postprocess(self, data):
        return data

    def handle(self, data, context):
        try:
            if not self.initialized:
                self.initialize(context)

            if data is None:
                return None
            
            data_parsed = data[0].get("body")
            if data_parsed is None:
                data_parsed = data[0].get("data")
            
            if isinstance(data_parsed, (bytes, bytearray)):
                text = data_parsed.decode("utf-8")

            text = self.preprocess(text)
            text = self.inference(text)
            text = self.postprocess(text)

            return text

        except Exception as e:
            raise e
