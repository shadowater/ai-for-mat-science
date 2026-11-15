#!/usr/bin/env python3
"""Export real 1024-dimensional embeddings and arithmetic for four classroom cases."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
from gguf import GGUFReader, dequantize
from inspect_embeddings import post

EXAMPLES = [
    ('国家与首都', '伦敦', '英国', '法国', '巴黎'),
    ('亲属称谓', '父亲', '母亲', '妈妈', '爸爸'),
    ('英文比较级', ' bigger', ' big', ' small', ' smaller'),
    ('英文进行式', ' walking', ' walk', ' run', ' running'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, default=Path.home()/'aimat/.local-llm/models/Qwen3-0.6B-Q8_0.gguf')
    parser.add_argument('--base-url', default='http://127.0.0.1:8087')
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    reader = GGUFReader(str(args.model))
    tensor = next(t for t in reader.tensors if t.name == 'token_embd.weight')
    E = dequantize(tensor.data, tensor.tensor_type).astype(np.float32, copy=False)
    norms = np.linalg.norm(E, axis=1)
    words = list(dict.fromkeys(w for case in EXAMPLES for w in case[1:]))
    ids = {}
    for word in words:
        tokens = post(args.base_url, '/tokenize', {'content':word, 'with_pieces':True,
                      'add_special':False, 'parse_special':False})['tokens']
        if len(tokens) != 1:
            raise ValueError(f'{word!r} must be a single token')
        ids[word] = tokens[0]['id']
    vec = lambda word: E[ids[word]]
    cos = lambda a,b: float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)))
    cases = []
    for title,b,a,c,d in EXAMPLES:
        q = vec(b)-vec(a)+vec(c)
        scores = (E@q)/(norms*np.linalg.norm(q)+1e-30)
        scores[[ids[w] for w in {a,b,c}]] = -np.inf
        nearest_id = int(np.argmax(scores))
        nearest_text = post(args.base_url, '/detokenize', {'tokens':[nearest_id]})['content']
        cases.append({'title':title, 'b':b,'a':a,'c':c,'target':d,
                      'query_vector':q.tolist(),
                      'source_difference':(vec(b)-vec(a)).tolist(),
                      'target_difference':(vec(d)-vec(c)).tolist(),
                      'nearest_token':nearest_text,'nearest_token_id':nearest_id,
                      'query_target_cosine':cos(q,vec(d)),
                      'difference_cosine':cos(vec(b)-vec(a),vec(d)-vec(c))})
    result = {'model':'Qwen3-0.6B Q8_0', 'tensor':'token_embd.weight',
              'dimension':int(E.shape[1]), 'quantization':'Q8_0 dequantized to float32',
              'notice':'Full vectors from the actual input table, not random or handcrafted. English leading spaces are part of tokens. Search excludes the three query input tokens.',
              'tokens':{w:{'id':ids[w],'vector':vec(w).tolist()} for w in words}, 'cases':cases}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir/'典型案例完整向量.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (args.output_dir/'典型词向量.csv').open('w',encoding='utf-8-sig',newline='') as file:
        writer=csv.writer(file, lineterminator="\n");writer.writerow(['token','token_id']+[f'd{i+1}' for i in range(E.shape[1])])
        for w in words:writer.writerow([w,ids[w],*vec(w).tolist()])
    print('Exported',len(words),'token vectors and',len(cases),'worked cases.')
    for case in cases:print(case['title'],repr(case['nearest_token']),case['query_target_cosine'])


if __name__=='__main__':main()
