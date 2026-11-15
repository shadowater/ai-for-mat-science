#!/usr/bin/env python3
"""Teaching harness: real local model choices, explicit Python tools, visible feedback."""
import argparse
from datetime import datetime
import json
import math
from pathlib import Path
import sys
import urllib.error
import urllib.request

ACTIONS = ['read_record', 'circle_area', 'write_report', 'finish']
ACTION_SCHEMA = {
    'type': 'object',
    'properties': {'action': {'type': 'string', 'enum': ACTIONS}},
    'required': ['action'], 'additionalProperties': False,
}
INSTRUCTIONS = '''你在使用工具完成任务。
可用工具：read_record 读取记录；circle_area 按已读取记录的半径计算面积；write_report 把已读取记录和已计算面积保存成报告；finish 结束。
每次只返回一个 JSON，如 {"action":"read_record"}。工具由程序执行，不要编造执行结果。'''


class Tools:
    def __init__(self, record_path, output_dir, task):
        self.record_path = record_path
        self.output_dir = output_dir
        self.task = task
        self.record = None
        self.area = None
        self.report = None

    def read_record(self):
        # A failed reread must not leave stale data eligible for later actions.
        self.record = self.area = self.report = None
        record = json.loads(self.record_path.read_text(encoding='utf-8'))
        if not isinstance(record, dict) or not isinstance(record.get('sample_id'), str):
            raise ValueError('记录需要字符串 sample_id。')
        radius = record.get('radius_mm')
        if isinstance(radius, bool) or not isinstance(radius, (int, float)):
            raise ValueError('radius_mm 必须是数值。')
        if not math.isfinite(radius) or radius < 0:
            raise ValueError('半径必须是非负有限数值。')
        self.record = record
        self.area = None
        self.report = None
        return {'sample_id': record['sample_id'], 'radius_mm': radius}

    def circle_area(self):
        if self.task == 'read':
            raise ValueError('当前是只读任务，不需要计算。')
        if self.record is None:
            raise ValueError('尚未读取记录，请先 read_record。')
        area = math.pi * self.record['radius_mm'] ** 2
        if not math.isfinite(area):
            raise ValueError('面积超出有限数值范围。')
        self.area = area
        return {'area_mm2': area, 'formula': 'pi * radius_mm ** 2'}

    def write_report(self):
        if self.task == 'read':
            raise ValueError('当前是只读任务，不允许保存报告。')
        if self.record is None or self.area is None:
            raise ValueError('缺少记录或计算结果，请先读取并计算。')
        content = (
            '# 教学样品面积报告\n\n'
            f"- 样品编号：{self.record['sample_id']}\n"
            f"- 半径：{self.record['radius_mm']} mm\n"
            f'- 圆面积：{self.area:.2f} mm²\n'
            '- 公式：A = πr²\n\n'
            '虚构教学数据；面积由 Python 工具计算，报告由固定模板生成，'
            '不代表接触角测量或真实实验结论。\n')
        path = self.output_dir / 'report.md'
        path.write_text(content, encoding='utf-8')
        if path.read_text(encoding='utf-8') != content:
            raise OSError('写入后核对失败。')
        self.report = path
        return {'saved': True, 'file': 'report.md', 'verified': True}

    def finish(self):
        if self.record is None:
            raise ValueError('还没有读取记录，不能宣布完成。')
        if self.task == 'report' and (self.report is None or not self.report.is_file()):
            raise ValueError('尚无已核对报告，不能宣布完成。')
        return {'completed': True, 'sample_id': self.record['sample_id'],
                'report': self.report.name if self.report else None}

    def dispatch(self, request):
        if not isinstance(request, dict) or set(request) != {'action'}:
            raise ValueError('请求必须只有一个 action 字段。')
        registry = {'read_record': self.read_record, 'circle_area': self.circle_area,
                    'write_report': self.write_report, 'finish': self.finish}
        action = request['action']
        if not isinstance(action, str) or action not in registry:
            raise ValueError('未知工具名。')
        return registry[action]()


def choose_action(base_url, messages):
    payload = {
        'messages': messages, 'stream': False, 'temperature': 0.7,
        'top_p': 0.8, 'top_k': 20, 'min_p': 0, 'seed': 42, 'max_tokens': 64,
        'chat_template_kwargs': {'enable_thinking': False},
        'response_format': {'type': 'json_schema', 'json_schema': {
            'name': 'next_action', 'strict': True, 'schema': ACTION_SCHEMA}},
    }
    request = urllib.request.Request(
        base_url.rstrip('/') + '/v1/chat/completions',
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=90) as response:
        result = json.load(response)
    return result['choices'][0]['message']['content']


def run(args):
    args.output_dir.mkdir(parents=True, exist_ok=False)
    tools = Tools(args.record, args.output_dir, args.task)
    task = ('只读取教学样品记录，读到后结束，不计算、不写报告。'
            if args.task == 'read' else '读取教学样品记录，按圆形计算面积，保存报告，然后结束。')
    order = ('只读取，随后结束。' if args.task == 'read' else '必须先读记录，再计算，再保存，最后结束。')
    messages = [{'role': 'user', 'content': INSTRUCTIONS + '\n任务：' + task + '\n' + order + '\n请选择下一步。'}]
    trace = {'task': args.task, 'model': 'Qwen3-0.6B Q8_0',
             'feedback_enabled': not args.drop_feedback,
             'instructions': messages[0]['content'], 'events': [], 'completed': False}
    try:
        for step in range(1, args.max_steps + 1):
            if args.pause:
                input(f'\n按 Enter 请求第 {step} 步（Ctrl+C 停止）…')
            event = {'step': step, 'messages_sent': [dict(m) for m in messages]}
            trace['events'].append(event)
            raw = choose_action(args.base_url, messages)
            event['model_output'] = raw
            print(f'\n[{step}] 模型请求：{raw}', flush=True)
            try:
                request = json.loads(raw)
                result = {'ok': True, 'result': tools.dispatch(request)}
            except (ValueError, TypeError, KeyError, OSError, OverflowError) as exc:
                result = {'ok': False, 'error': str(exc)}
            event['tool_result'] = result
            print('    Harness 执行结果：' + json.dumps(result, ensure_ascii=False), flush=True)
            # Completion is accepted only from a successfully checked finish request.
            if result['ok'] and request['action'] == 'finish':
                trace['completed'] = True
                break
            messages.append({'role': 'assistant', 'content': raw})
            if args.drop_feedback:
                messages.append({'role': 'user', 'content': '工具结果未加入上下文。请决定下一步。'})
            else:
                messages.append({'role': 'user', 'content':
                    '工具结果：' + json.dumps(result['result'] if result['ok'] else result, ensure_ascii=False) + '。请选择下一步。'})
        if not trace['completed']:
            trace['stop_reason'] = '达到步数上限，未完成；没有替模型补齐后续操作。'
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as exc:
        trace['stop_reason'] = f'模型接口失败：{exc}'
    except (KeyboardInterrupt, EOFError):
        trace['stop_reason'] = '教师停止演示。'
    finally:
        (args.output_dir / 'trace.json').write_text(
            json.dumps(trace, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('\nHarness 确认：' + ('任务完成。' if trace['completed'] else trace['stop_reason']))
    print('执行记录：' + str(args.output_dir / 'trace.json'))
    if tools.report:
        print('实际报告：' + str(tools.report))
    return 0 if trace['completed'] else 1


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='http://127.0.0.1:8087')
    parser.add_argument('--record', type=Path, default=here / 'data' / 'sample.json')
    parser.add_argument('--task', choices=['report', 'read'], default='report')
    parser.add_argument('--max-steps', type=int, default=8)
    parser.add_argument('--pause', action='store_true')
    parser.add_argument('--drop-feedback', action='store_true', help='Omit tool results as a teaching contrast.')
    parser.add_argument('--output-dir', type=Path,
                        default=here / 'outputs' / datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    args = parser.parse_args()
    if not 1 <= args.max_steps <= 20:
        parser.error('--max-steps must be between 1 and 20')
    try:
        return run(args)
    except OSError as exc:
        print(f'无法建立新的输出目录：{exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
