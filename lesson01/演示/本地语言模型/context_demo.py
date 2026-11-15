#!/usr/bin/env python3
"""Compare explicit context inputs using the existing local model service."""
import argparse
import json
from pathlib import Path
import sys
import urllib.error
from inspect_llm import post


def cases(record):
    question = '样品编号是什么？请只回答编号。'
    user = {'role': 'user', 'content': question}
    return [
        ('没有记录', [user]),
        ('带上历史记录', [
            {'role': 'user', 'content': record},
            {'role': 'assistant', 'content': '收到记录。'}, user]),
        ('丢掉历史只发末句', [user]),
        ('只提供文件名', [{'role': 'user', 'content':
            '请从教学样品记录.txt读取样品编号。请只回答编号。'}]),
        ('脚本实际读取文件后提供正文', [{'role': 'user', 'content':
            f'以下是程序读取的教学样品记录.txt正文：\n{record}\n\n{question}'}]),
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='http://127.0.0.1:8087')
    parser.add_argument('--output', type=Path, help='Optional JSON report destination.')
    args = parser.parse_args()
    record_path = Path(__file__).with_name('教学样品记录.txt')
    record = record_path.read_text(encoding='utf-8').strip()
    results = []
    try:
        for title, messages in cases(record):
            with post(args.base_url, '/apply-template', {
                    'messages': messages, 'add_generation_prompt': True,
                    'chat_template_kwargs': {'enable_thinking': False}}) as response:
                prompt = json.load(response)['prompt']
            with post(args.base_url, '/tokenize', {
                    'content': prompt, 'add_special': False, 'parse_special': True}) as response:
                count = len(json.load(response)['tokens'])
            with post(args.base_url, '/v1/chat/completions', {
                    'messages': messages, 'stream': False, 'max_tokens': 96,
                    'temperature': 0.7, 'top_p': 0.8, 'top_k': 20, 'min_p': 0,
                    'seed': 42, 'chat_template_kwargs': {'enable_thinking': False}}) as response:
                result = json.load(response)
            answer = result['choices'][0]['message']['content']
            results.append({'case': title, 'messages': messages,
                            'formatted_prompt': prompt,
                            'formatted_prompt_tokens': count,
                            'answer': answer, 'usage': result.get('usage')})
            print(f'\n【{title}】消息 {len(messages)} 条，模板文本 {count} tokens\n回答：{answer}')
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as exc:
        print(f'本地演示失败：{exc}。请确认服务已启动；不会改用在线模型。', file=sys.stderr)
        return 1
    if args.output:
        args.output.write_text(json.dumps({
            'notice': '真实本地请求与输出。数据为虚构教学记录；失败与猜测均原样保留。',
            'model': 'Qwen3-0.6B Q8_0', 'temperature': 0.7, 'seed': 42,
            'cases': results}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'\n已保存：{args.output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
