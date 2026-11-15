#!/usr/bin/env python3
"""Batch analogy searches on the deployed model; keep failed and split-token cases."""
import argparse
from itertools import permutations
import json
from pathlib import Path
import time
import numpy as np
from gguf import GGUFReader, dequantize
from inspect_embeddings import post


def make_cases():
    # Categories inspired by word2vec's original analogy tasks, not its full benchmark.
    groups = {
        '中文国家到首都': [('中国','北京'),('日本','东京'),('法国','巴黎'),('德国','柏林'),
                       ('英国','伦敦'),('意大利','罗马'),('俄罗斯','莫斯科'),('西班牙','马德里')],
        '英文国家到首都': [('China','Beijing'),('Japan','Tokyo'),('France','Paris'),('Germany','Berlin')],
        '英文复数': [('cat','cats'),('dog','dogs'),('car','cars')],
        '英文进行式_含前导空格': [(' walk',' walking'),(' run',' running'),(' swim',' swimming')],
        '英文比较级_含前导空格': [(' big',' bigger'),(' small',' smaller'),(' cold',' colder'),(' happy',' happier')],
        '英文不规则比较级_含前导空格': [(' good',' better'),(' bad',' worse')],
        '英文副词_含前导空格': [(' quick',' quickly'),(' slow',' slowly')],
        '亲属性别关系': [('女人','男人'),('母亲','父亲'),('姐姐','哥哥'),('妹妹','弟弟'),
                      ('女王','国王'),('公主','王子'),('妻子','丈夫'),('妈妈','爸爸'),('女儿','儿子')],
        '中文反义关系_探索': [('大','小'),('长','短'),('高','低'),('热','冷'),('快','慢')],
        '国家到语言_探索': [('法国','法语'),('德国','德语'),('日本','日语'),('韩国','韩语')],
    }
    cases=[]
    for category,pairs in groups.items():
        for (a,b),(c,d) in permutations(pairs,2):
            cases.append({'category':category,'a':a,'b':b,'c':c,'expected':d})
    return cases


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model',type=Path,default=Path.home()/'aimat/.local-llm/models/Qwen3-0.6B-Q8_0.gguf')
    parser.add_argument('--base-url',default='http://127.0.0.1:8087')
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('扩展实测结果.json'))
    args=parser.parse_args();start=time.perf_counter()
    cases=make_cases();tokenization={}
    for word in dict.fromkeys(word for c in cases for word in [c['a'],c['b'],c['c'],c['expected']]):
        tokenization[word]=post(args.base_url,'/tokenize',{'content':word,'with_pieces':True,
                                       'add_special':False,'parse_special':False})['tokens']
    valid=[];skipped=[]
    for c in cases:
        split=[w for w in [c['a'],c['b'],c['c'],c['expected']] if len(tokenization[w])!=1]
        if split:skipped.append(dict(c,reason='not_single_token',split_words=split))
        else:valid.append(c)
    reader=GGUFReader(str(args.model));t=next(t for t in reader.tensors if t.name=='token_embd.weight')
    E=dequantize(t.data,t.tensor_type).astype(np.float32,copy=False)
    norms=np.linalg.norm(E,axis=1)
    ids={w:pieces[0]['id'] for w,pieces in tokenization.items() if len(pieces)==1}
    vectors=lambda w:E[ids[w]]
    queries=np.stack([vectors(c['b'])-vectors(c['a'])+vectors(c['c']) for c in valid])
    all_queries=queries
    all_queries/=np.maximum(np.linalg.norm(all_queries,axis=1,keepdims=True),1e-30)
    numeric_start=time.perf_counter()
    # Batch matrix multiply is much cheaper than issuing hundreds of separate searches.
    scores=all_queries@E.T
    scores/=np.maximum(norms[None,:],1e-30)
    matrix_seconds=time.perf_counter()-numeric_start
    n=len(valid);results=[];decoded={}
    for i,c in enumerate(valid):
        row=scores[i]
        exclude=[ids[w] for w in {c['a'],c['b'],c['c']}]
        row[exclude]=-np.inf
        target=ids[c['expected']]
        if target in exclude:
            skipped.append(dict(c,reason='answer_in_excluded_query_inputs'));continue
        rank=int(np.count_nonzero(row>row[target])+1)
        top=np.argpartition(row,-5)[-5:];top=top[np.argsort(row[top])[::-1]]
        neighbors=[]
        for index in top:
            index=int(index)
            if index not in decoded:decoded[index]=post(args.base_url,'/detokenize',{'tokens':[index]})['content']
            neighbors.append({'token_id':index,'text':decoded[index],'cosine':float(row[index])})
        d1=vectors(c['b'])-vectors(c['a']);d2=vectors(c['expected'])-vectors(c['c'])
        direction_cosine=float(np.dot(d1,d2)/(np.linalg.norm(d1)*np.linalg.norm(d2)))
        results.append(dict(c,query=f"{c['b']} - {c['a']} + {c['c']}",
                            expected_rank=rank,
                            difference_cosine=direction_cosine,nearest=neighbors))
    result={'model':'Qwen3-0.6B Q8_0','tensor':'token_embd.weight','shape':list(E.shape),
            'method':'Raw input embedding offsets; cosine retrieval over full vocabulary excluding three query tokens. No averaging split words, no contextual forward pass, no PCA.',
            'source_categories':'https://github.com/tmikolov/word2vec/blob/master/questions-words.txt',
            'notice':'Selected classroom probes, including Chinese adaptations and exploratory antonyms/languages; not the original full benchmark or a general model accuracy estimate. Leading spaces in English are part of token identity.',
            'matrix_seconds':matrix_seconds,'total_seconds':time.perf_counter()-start,
            'tokenization':tokenization,'results':results,'skipped':skipped}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Probes:',len(cases),'evaluated:',len(results),'skipped:',len(skipped),flush=True)
    print('Matrix seconds:',round(matrix_seconds,3),'total seconds:',round(result['total_seconds'],3),flush=True)
    for c in sorted(results,key=lambda r:(r['expected_rank']!=1,-r['difference_cosine']))[:22]:
        print(c['category'],repr(c['query']),'->',repr(c['nearest'][0]['text']),
              'target rank',c['expected_rank'],'direction cosine',round(c['difference_cosine'],3))


if __name__=='__main__':main()
