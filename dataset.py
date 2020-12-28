# Importing libraries
import os
#import numpy as np
#import pandas as pd
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, RandomSampler, SequentialSampler
import sentencepiece

# Importing the T5 modules from huggingface/transformers
from transformers import T5Tokenizer, T5ForConditionalGeneration

'''Creating a custom dataset for reading the dataset and 
loading it into the dataloader to pass it to the neural network for finetuning the model'''

class HeadlinesDataset(Dataset):

    def __init__(self, dataframe, tokenizer, source_len, summ_len):
        self.tokenizer = tokenizer
        self.data = dataframe
        self.source_len = source_len
        self.summ_len = summ_len
        self.headlines = self.data.headlines
        self.ctext = self.data.ctext

    def __len__(self):
        return len(self.headlines)

    def __getitem__(self, index):
        ctext = str(self.ctext[index])
        headlines = str(self.headlines[index])

        #cleaning data so as to ensure data is in string type
        ctext = ' '.join(ctext.split())
        headlines = ' '.join(headlines.split())

        source = self.tokenizer.batch_encode_plus([ctext], max_length= self.source_len, pad_to_max_length=True,return_tensors='pt')
        target = self.tokenizer.batch_encode_plus([headlines], max_length= self.summ_len, pad_to_max_length=True,return_tensors='pt')

        source_ids = source['input_ids'].squeeze()
        source_mask = source['attention_mask'].squeeze()
        target_ids = target['input_ids'].squeeze()
        target_mask = target['attention_mask'].squeeze()

        return {
            'source_ids': source_ids.to(dtype=torch.long), 
            'source_mask': source_mask.to(dtype=torch.long), 
            'target_ids': target_ids.to(dtype=torch.long),
            'target_ids_y': target_ids.to(dtype=torch.long)
        }