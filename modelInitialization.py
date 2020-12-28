import torch
import json 
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
import sentencepiece
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, RandomSampler, SequentialSampler
from torch import cuda

# Method for initializing models and tokenizers at the start of server
# so that subsequent calls do not get slowed down because of these start up steps
def initialize_model_and_tokenizer(modelName = 't5-small'):
    # Setting up the device for GPU usage
    device = 'cuda' if cuda.is_available() else 'cpu'
    model = T5ForConditionalGeneration.from_pretrained(modelName)
    heading_model = torch.load('model/heading_model.pth' if device == 'cuda' else 'model/heading_model_cpu.pth')
    tokenizer = T5Tokenizer.from_pretrained(modelName)
    return device, model, heading_model, tokenizer