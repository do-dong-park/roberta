from transformers import AutoTokenizer, AutoModelForSequenceClassification

# instantiating the tokenizer associated with the model
tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")

# Creating the model instance
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")

# save the tokenizer instance
tokenizer.save_pretrained('../my_tokenizer')

# save the model instance
model.save_pretrained('../my_model')