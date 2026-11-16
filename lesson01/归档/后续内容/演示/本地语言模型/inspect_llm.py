#!/usr/bin/env python3
"""Inspect a local llama-server. Python standard library only; no model bundled."""
import argparse
import json
import sys
import urllib.error
import urllib.request


def post(base_url, path, payload, timeout=120):
    request = urllib.request.Request(
        base_url.rstrip('/') + path,
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'}, method='POST')
    return urllib.request.urlopen(request, timeout=timeout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['tokens', 'next', 'chat'])
    parser.add_argument('--base-url', default='http://127.0.0.1:8087')
    parser.add_argument('--text', default='样品编号是 M-02。')
    parser.add_argument('--temperature', type=float, default=0.7)
    args = parser.parse_args()
    if args.temperature < 0:
        parser.error('temperature must be nonnegative')
    try:
        if args.mode == 'tokens':
            with post(args.base_url, '/tokenize', {
                    'content': args.text, 'with_pieces': True,
                    'add_special': False, 'parse_special': False}) as response:
                result = json.load(response)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.mode == 'next':
            # Raw continuation, intentionally not wrapped as a chat instruction.
            with post(args.base_url, '/completion', {
                    'prompt': args.text, 'n_predict': 1, 'stream': False,
                    'temperature': args.temperature, 'n_probs': 5,
                    'post_sampling_probs': False, 'return_tokens': True,
                    'seed': 42}) as response:
                result = json.load(response)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # Chat template and non-thinking switch are interpreted by the server.
            with post(args.base_url, '/v1/chat/completions', {
                    'messages': [{'role': 'user', 'content': args.text}],
                    'max_tokens': 128, 'temperature': args.temperature,
                    'top_p': 0.8, 'top_k': 20, 'min_p': 0,
                    'chat_template_kwargs': {'enable_thinking': False},
                    'stream': True, 'seed': 42}) as response:
                for line in response:
                    if not line.startswith(b'data:'):
                        continue
                    event = line[5:].strip()
                    if event == b'[DONE]':
                        break
                    item = json.loads(event)
                    if 'error' in item:
                        raise RuntimeError(item['error'])
                    for choice in item.get('choices', []):
                        delta = choice.get('delta', {})
                        if delta.get('reasoning_content'):
                            print(delta['reasoning_content'], end='', flush=True)
                        if delta.get('content'):
                            print(delta['content'], end='', flush=True)
            print()
    except (urllib.error.URLError, TimeoutError, ValueError, RuntimeError) as exc:
        print(f'本地模型请求失败：{exc}\n请先启动 llama-server，并核对地址与端口。', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
