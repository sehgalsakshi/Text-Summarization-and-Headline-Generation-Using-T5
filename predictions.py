''' Method to summarize text(or heading) in abstractive manner
Device, model, tokenizer and original text are given as input
And it first encodes using same tokenizer that was used for model creation
And passes this as input to model for getting text summary predictions'''
def predict(device, model, tokenizer, text, max_length = 100, min_length = 30):
    preprocess_text = text.strip().replace("\n","")
    t5_prepared_Text = "summarize: "+preprocess_text
    tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)
    # summmarize 
    summary_ids = model.generate(tokenized_text,
                                        num_beams=4,
                                        no_repeat_ngram_size=2,
                                        min_length=min_length,
                                        max_length=max_length,
                                        early_stopping=True)

    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return output