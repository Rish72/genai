import tiktoken

enc = tiktoken.encoding_for_model('gpt-4o')

encoded = enc.encode("This is my first test")
print("Vocab size ", enc.n_vocab)
print("Encoded data ", encoded)