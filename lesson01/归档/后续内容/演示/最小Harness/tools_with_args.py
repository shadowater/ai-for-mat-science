#!/usr/bin/env python3
"""One real model-generated parameterized request, local execution, and feedback."""
import argparse
from datetime import datetime
import json
import math
from pathlib import Path
import sys
import urllib.error
import urllib.request

REQUEST_SCHEMA = {
    'type': 'object', 'properties': {
        'name': {'type': 'string', 'enum': ['circle_area']},
        'arguments': {'type': 'object', 'properties': {
            'radius_mm': {'type': 'number'}},
            'required': ['radius_mm'], 'additionalProperties': False}},
    'required': ['name', 'arguments'], 'additionalProperties': False,
}


def circle_area(radius_mm):
    if isinstance(radius_mm, bool) or not isinstance(radius_mm, (int, float)):
        raise ValueError('radius_mm 必须是数值，单位 mm。')
    if not math.isfinite(radius_mm) or radius_mm < 0:
        raise ValueError('半径必须是非负有限数值，不能自动删除负号。')
    area = math.pi * radius_mm ** 2
    if not math.isfinite(area):
        raise ValueError('面积超出有限数值范围。')
    return {'radius_mm': radius_mm, 'area_mm2': area}


def dispatch(request):
    if not isinstance(request, dict) or set(request) != {'name', 'arguments'}:
        raise ValueError('需要且只允许 name、arguments 两个字段。')
    if request['name'] != 'circle_area':
        raise ValueError('工具未注册。')
    args = request['arguments']
    if not isinstance(args, dict) or set(args) != {'radius_mm'}:
        raise ValueError('需要且只允许 radius_mm 参数。')
    return circle_area(args['radius_mm'])


def model_request(base_url, messages, schema=None):
    payload = {'messages': messages, 'stream': False,
               'temperature': 0.7, 'top_p': 0.8, 'top_k': 20, 'min_p': 0,
               'seed': 42, 'max_tokens': 160,
               'chat_template_kwargs': {'enable_thinking': False}}
    if schema:
        payload['response_format'] = {'type': 'json_schema', 'json_schema': {
            'name': 'tool_request', 'strict': True, 'schema': schema}}
    req = urllib.request.Request(base_url.rstrip('/') + '/v1/chat/completions',
                                 data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
                                 headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=90) as response:
        return json.load(response)['choices'][0]['message']['content']


def run(args):
    args.output_dir.mkdir(parents=True, exist_ok=False)
    prompt = (f'工具 circle_area 的参数 radius_mm 是数值，单位 mm。'
              f'任务：请求计算半径为 {args.radius_mm} mm 的圆面积。'
              '只返回包含 name 和 arguments 的 JSON，不要自行计算面积。'
              '参数必须保持题目给定值，负数也必须保留负号，工具会检查。')
    messages = [{'role': 'user', 'content': prompt}]
    trace = {'mode': 'custom_json_not_native_tool_calls', 'messages_sent': messages.copy(),
             'expected_radius_mm': args.radius_mm, 'executed': False, 'completed': False}
    try:
        raw = model_request(args.base_url, messages, REQUEST_SCHEMA)
        trace['model_request'] = raw
        print('模型生成的调用请求：' + raw, flush=True)
        request = json.loads(raw)
        if args.pause:
            input('此时尚未执行工具。按 Enter 继续执行，Ctrl+C 停止…')
        if args.skip_execution:
            trace['stop_reason'] = '只生成请求；没有执行工具，也没有请求最终回答。'
            print(trace['stop_reason'])
            return 0
        try:
            # Check preservation separately from input validity, so errors stay visible.
            if request.get('arguments', {}).get('radius_mm') != args.radius_mm:
                raise ValueError('模型参数与任务给定半径不一致，不执行修改后的任务。')
            result = {'ok': True, 'result': dispatch(request)}
            trace['executed'] = True
        except (ValueError, TypeError, OverflowError) as exc:
            result = {'ok': False, 'error': str(exc)}
        trace['tool_result'] = result
        print('Python 工具／Harness 结果：' + json.dumps(result, ensure_ascii=False), flush=True)
        messages.append({'role': 'assistant', 'content': raw})
        messages.append({'role': 'user', 'content':
                         '实际执行结果：' + json.dumps(result, ensure_ascii=False) +
                         '。请用一句中文说明结果；失败就说明失败，不要改半径或编造面积。'})
        trace['final_messages_sent'] = messages.copy()
        answer = model_request(args.base_url, messages)
        trace['model_answer'] = answer
        print('模型根据反馈回答：' + answer, flush=True)
        trace['completed'] = result['ok']
        print('程序核对：' + ('面积计算成功；模型措辞仍需人工核对。' if result['ok'] else '参数被拒绝，没有有效面积结果。'))
        return 0 if result['ok'] else 1
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError, AttributeError) as exc:
        trace['stop_reason'] = f'演示失败：{exc}'
        print(trace['stop_reason'], file=sys.stderr)
        return 1
    except (KeyboardInterrupt, EOFError):
        trace['stop_reason'] = '教师停止，未继续执行。'
        return 1
    finally:
        (args.output_dir / 'trace.json').write_text(
            json.dumps(trace, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print('记录：' + str(args.output_dir / 'trace.json'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='http://127.0.0.1:8087')
    parser.add_argument('--radius-mm', type=float, default=2)
    parser.add_argument('--pause', action='store_true')
    parser.add_argument('--skip-execution', action='store_true')
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent /
                        'outputs' / ('args-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f')))
    args = parser.parse_args()
    if not math.isfinite(args.radius_mm):
        parser.error('--radius-mm 必须为有限数值。')
    try:
        return run(args)
    except OSError as exc:
        print(f'输出目录不可用：{exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
