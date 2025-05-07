from transformers import AutoModel, AutoTokenizer
import torch
import json
import os

def model_fn(model_dir):
    # Load the model from the directory provided by SageMaker
    print(model_dir)
    print(os.listdir(model_dir))
    model = AutoModel.from_pretrained(model_dir)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    return model, tokenizer

def input_fn(request_body, content_type='application/json'):
    if content_type == 'application/json':
        input_data = json.loads(request_body)
        return input_data['inputs']
    else:
        raise ValueError(f"Unsupported content type: {content_type}")

def predict_fn(input_data, model_and_tokenizer):
    model, tokenizer = model_and_tokenizer
    #print(input_data)

    try:
        if isinstance(input_data, str):
            input_text = input_data
        elif isinstance(input_data, dict):
            input_text = input_data['text']

    except Exception as e:
        print(input_data)
        print('Input is not either str or dict with "text" key')
        raise

    # Chunk input text -- if short text, just turns into len-1 list
    chunks = chunk_text(input_text, tokenizer)
    if len(chunks) > 1:
        print(f'Needed to split input text into {len(chunks)} chunks to keep under {512} tokens')
        print('This may lead to a failure to return properly')
        for i in range(len(chunks)):
            print('Chunk', i, 'len', len(tokenizer.tokenize(chunks[i])))

    # Loop over all chunks
    final_output = [] # shape [n_chunks, n_tokenz, X]
    for chunk in chunks:

        # Tokenize input text
        inputs = tokenizer(chunk, return_tensors="pt", padding=True, truncation=True)
        
        # Run the model to get embeddings
        with torch.no_grad():
            outputs = model(**inputs)

        # Return the embeddings as a list and avg to coalesce into 1-D list
        embeddings = outputs.last_hidden_state[0] # shape: [num_tokens, hidden_size]

        # Append to final output
        final_output.append(embeddings)
    
    # Concatenate e.g. [501, X] + [39, X] --> [540, X]
    final_output = torch.cat(final_output, dim=0) # shape: [num_tokens_FULLPAGE, X]

    # Take avg and return
    final_output = final_output.mean(dim=0).tolist() # shape: [X]
    
    return {"embeddings": final_output}

def output_fn(prediction, accept='application/json'):
    return json.dumps({"predictions": prediction})

def chunk_text(text, tokenizer, chunk_size=500, overlap=50):
    """
    Splits a long text into overlapping chunks of tokens.
    If the text is small enough to fit into a single chunk (<512 tokens),
    all that's done is to return as a list.

    Args:
        text (str): The long text to be split.
        tokenizer (PreTrainedTokenizer): The tokenizer to use for splitting.
        chunk_size (int): The maximum number of tokens per chunk (default 512).
        overlap (int): The number of tokens to overlap between consecutive chunks (default 50).

    Returns:
        chunks (list): List of strings corresponding to each chunk.
    """
    tokens = tokenizer.tokenize(text)
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk_tokens = tokens[i:i + chunk_size]
        chunk_text = tokenizer.convert_tokens_to_string(chunk_tokens)
        chunks.append(chunk_text)
    return chunks