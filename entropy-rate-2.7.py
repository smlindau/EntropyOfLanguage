import re, codecs, random, math, textwrap, os
from collections import defaultdict, deque, Counter

def tokenize(file_path, tokenizer):
	with codecs.open(file_path, mode="r", encoding="utf-8") as file:
		for line in file:
			for token in tokenizer(line.lower().strip()):
				yield token
				
def chars(file_path):
	return tokenize(file_path, lambda s: s + " ")
	
def words(file_path):
	return tokenize(file_path, lambda s: re.findall(r"[^:punct:]+", s))

def markov_model(stream, model_order):
	model, stats = defaultdict(Counter), Counter()
	circular_buffer = deque(maxlen = model_order)
	
	for token in stream:
		prefix = tuple(circular_buffer)
		circular_buffer.append(token)
		if len(prefix) == model_order:
			stats[prefix] += 1.0
			model[prefix][token] += 1.0
	return model, stats

def entropy(stats, normalization_factor):
	return -sum(proba / normalization_factor * math.log(proba / normalization_factor, 2) for proba in stats.values())

def entropy_rate(model, stats):
	return sum(stats[prefix] * entropy(model[prefix], stats[prefix]) for prefix in stats) / sum(stats.values())

for x in range(1, 9):
    model, stats = markov_model(chars("*.txt"), x)
    print entropy_rate(model, stats)
