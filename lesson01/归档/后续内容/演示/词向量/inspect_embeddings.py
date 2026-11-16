#!/usr/bin/env python3
"""Inspect static input embeddings in the actual quantized classroom model."""
import argparse
import json
from pathlib import Path
import urllib.request
import numpy as np
from gguf import GGUFReader, dequantize


def post(base, path, payload):
    req = urllib.request.Request(base.rstrip('/') + path,
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, default=Path.home() / 'aimat/.local-llm/models/Qwen3-0.6B-Q8_0.gguf')
    parser.add_argument('--base-url', default='http://127.0.0.1:8087')
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('实测结果.json'))
    args = parser.parse_args()
    pairs = [('男人','女人'),('叔叔','阿姨'),('父亲','母亲'),('哥哥','姐姐'),
             ('弟弟','妹妹'),('国王','女王'),('男孩','女孩'),('他','她'),('男','女')]
    token_ids = {}
    for word in dict.fromkeys(w for pair in pairs for w in pair):
        pieces = post(args.base_url, '/tokenize', {'content': word, 'add_special': False,
                      'parse_special': False, 'with_pieces': True})['tokens']
        if len(pieces) != 1:
            raise ValueError(f'{word!r} is not a single token: {pieces}')
        token_ids[word] = pieces[0]['id']
    print('Reading and dequantizing actual token_embd.weight ...', flush=True)
    reader = GGUFReader(str(args.model))
    tensor = next(t for t in reader.tensors if t.name == 'token_embd.weight')
    embeddings = dequantize(tensor.data, tensor.tensor_type).astype(np.float32, copy=False)
    assert embeddings.shape == (151936, 1024), embeddings.shape
    norms = np.linalg.norm(embeddings, axis=1)
    def vector(word):
        return embeddings[token_ids[word]]
    def cosine(a,b):
        return float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)))
    direction = vector('男人') - vector('女人')
    relations, analogies = [], []
    for male,female in pairs:
        delta = vector(male)-vector(female)
        relation = {'pair': [male,female], 'difference_cosine_with_man_minus_woman': cosine(direction,delta),
                    'difference_norm': float(np.linalg.norm(delta)),
                    'residual_relative_to_mean_difference_norm': float(
                        np.linalg.norm(direction-delta)/((np.linalg.norm(direction)+np.linalg.norm(delta))/2))}
        relations.append(relation)
        if male == '男人':
            continue
        query = vector(female)+direction
        scores = (embeddings @ query) / (norms*np.linalg.norm(query) + 1e-30)
        # Exclude the three query inputs, to avoid returning the unchanged anchor.
        excluded = [token_ids[w] for w in {'男人','女人',female}]
        scores[excluded] = -np.inf
        target_rank = int(np.count_nonzero(scores > scores[token_ids[male]]) + 1)
        ids = np.argsort(scores)[-8:][::-1]
        neighbors = []
        for token_id in ids:
            text = post(args.base_url, '/detokenize', {'tokens': [int(token_id)]})['content']
            neighbors.append({'id':int(token_id),'text':text,'cosine':float(scores[token_id])})
        analogies.append({'query':f'{female} + 男人 - 女人', 'expected':male,
                         'expected_rank':target_rank,
                         'expected_cosine':float(scores[token_ids[male]]),
                         'excluded_input_words':['男人','女人',female], 'nearest_tokens':neighbors})
        print(male,female,'direction cosine',round(relation['difference_cosine_with_man_minus_woman'],4),
              'expected rank',target_rank,'top',[n['text'] for n in neighbors[:3]],flush=True)
    result = {'model':'Qwen3-0.6B Q8_0',
              'model_sha256':'9465e63a22add5354d9bb4b99e90117043c7124007664907259bd16d043bb031',
              'tensor':'token_embd.weight','quantization':'Q8_0 dequantized to float32',
              'shape':list(embeddings.shape),'token_ids':token_ids,
              'method':'Raw input embedding arithmetic; cosine retrieval over all vocabulary rows; exclude query input tokens. No centering, no PCA, no contextual forward pass.',
              'relations':relations,'analogies':analogies}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Saved',args.output)


if __name__ == '__main__':
    main()
