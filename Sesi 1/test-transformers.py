from transformers import pipeline

p = pipeline(
    "sentiment-analysis",
    model = "distilbert-base-uncased-finetuned-sst-2-english"
)

result = p(" I love learning AI!")

print(result)