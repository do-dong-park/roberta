import torch
import logging
import os
import json
import requests
import datetime
import sys

from log_db.chat_log import TorchServeDB
from ts.torch_handler.base_handler import BaseHandler
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# creating a logger
logger = logging.getLogger(__name__)

# custom  model handler class
class ModelHandler(BaseHandler):
    def __init__(self):
        # 현재 스크립트 파일의 경로 가져오기

        self.input = None
        self.request_ip = None

    def initialize(self, context):
        properties = context.system_properties
        self.manifest = context.manifest
        model_dir = properties.get("model_dir")

        # use GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # load the model
        model_file = self.manifest["model"]["modelFile"]
        model_path = os.path.join(model_dir, model_file)

        if os.path.isfile(model_path):
            self.model = AutoModelForSequenceClassification.from_pretrained(model_dir)
            self.model.to(self.device)
            self.model.eval()  # to  be used for inference

        else:
            raise RuntimeError("model file missing")

        # load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        if self.tokenizer is None:
            raise RuntimeError("Missing the tokenizer object")

        # load the mapping file
        mapping_file_path = os.path.join(model_dir, "index_to_name.json")

        if os.path.isfile(mapping_file_path):
            with open(mapping_file_path) as f:
                self.mapping = json.load(f)

        else:
            logger.warning("Mapping file missing")

        self.initialized = True

    def preprocess(self, requests):
        # unpack
        data = requests[0].get("body")
        if data is None:
            data = requests[0].get("data")

        inp_x = data.get("inputs")

        self.input = inp_x
        # tokenize
        tokenized_inp = self.tokenizer(inp_x, padding=True, return_tensors="pt")

        logger.info("Tokenization completed!")

        return tokenized_inp

    def inference(self, inputs):
        outputs = self.model(**inputs.to(self.device))
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        preds = torch.argmax(probs, axis=1)
        preds = preds.tolist()
        logger.info("Predictions generated!")

        return preds

    def postprocess(self, outputs: list):
        preds = [self.mapping[str(label)] for label in outputs]
        logger.info(f"Predicted Labels: {preds}")

        # 추론 정보 저장
        log_info = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "client_ip": self.context.get_request_header(0, "Host"),
            "input_data": self.input,
            "output_data": preds,
        }
        # DB에 요청 정보 기록
        logger.info(f"save logs : {log_info}")

        torchserve_db = TorchServeDB()
        torchserve_db.save_log(log_info)

        return [preds]
