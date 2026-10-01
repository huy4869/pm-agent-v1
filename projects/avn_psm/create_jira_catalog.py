"""Create the user-reviewed KHDS_SP catalog without modifying its source workbook."""
import argparse
import json
from pathlib import Path

import requests
from dotenv import dotenv_values

PROJECT = 'AVN_PSM_AKAMES_2026_PM'
BASE = 'https://fis-pro360.fpt.com/jira/rest/api/2'
VERSIONS = [
    ('Khởi động và khảo sát', '2026-09-01', '2026-09-30'),
    ('Thiết kế', '2026-10-01', '2026-11-30'),
    ('Kiểm thử', '2026-12-01', '2026-12-30'),
    ('Triển khai', '2026-11-30', '2026-12-30'),
]
COMPONENTS = [
    '-Kế hoạch KH, Slide & BBH kickoff\n-Bộ kế hoạch nội bộ (KHCF, KHDS, KHCH,KHCL)',
    'Sơ đồ quy trình',
    'Bản tổng hợp yêu cầu nghiệp vụ',
    'RMSheet giai đoạn khởi động',
    'Tài liệu thiết kế giải pháp và kỹ thuật tổng thể',
    'Testcase GAP',
    'Gói phần mềm đã phát triển',
    'Tài liệu HDSD hệ thống',
    'RMSheet giai đoạn thiết kế',
    'Testcase UAT',
    'Kế hoạch UAT',
    'BBNT UAT',
    'RMSheet giai đoạn kiểm thử',
    'Kế hoạch golive',
    'Checklist kiểm tra an toàn thông tin trước khi triển khai ứng dụng cho golive',
    'Biên bản xác nhận hoàn thành golive',
    'Báo cáo tổng kết dự án',
]


def normalized(name):
    return ''.join(name.split()).lstrip('-').casefold()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    env = dotenv_values(Path(__file__).resolve().parents[2] / '.env')
    assert env['JIRA_PROJECT_KEY'] == PROJECT, 'Unexpected project in env'
    session = requests.Session()
    session.headers.update({'Authorization': 'Bearer ' + env['JIRA_API_TOKEN'], 'Accept': 'application/json'})

    def api(method, path, body=None):
        response = session.request(method, BASE + path, json=body, timeout=30, allow_redirects=False)
        if not response.ok:
            raise RuntimeError(f'{method} {path}: HTTP {response.status_code}: {response.text[:1000]}')
        return response.json() if response.content else None

    versions = api('GET', f'/project/{PROJECT}/versions')
    components = api('GET', f'/project/{PROJECT}/components')
    for name, start, end in VERSIONS:
        matches = [v for v in versions if normalized(v['name']) == normalized(name)]
        assert len(matches) <= 1, f'Ambiguous version: {name}'
        payload = {'name': name, 'project': PROJECT, 'startDate': start, 'releaseDate': end}
        if matches:
            v = matches[0]
            assert v.get('startDate') == start and v.get('releaseDate') == end, f'Existing version date conflict: {name}'
            action = 'existing'
        elif args.apply:
            v = api('POST', '/version', payload)
            action = 'created'
        else:
            v = payload
            action = 'would_create'
        if args.apply:
            v = api('GET', '/version/' + str(v['id']))
            assert v['name'] == name and v.get('startDate') == start and v.get('releaseDate') == end
        print(json.dumps({'kind': 'version', 'action': action, 'data': {k: v.get(k) for k in ('id', 'name', 'startDate', 'releaseDate')}}, ensure_ascii=False))

    for name in COMPONENTS:
        matches = [c for c in components if normalized(c['name']) == normalized(name)]
        assert len(matches) <= 1, f'Ambiguous component: {name}'
        payload = {'name': name, 'project': PROJECT, 'assigneeType': 'PROJECT_LEAD'}
        if matches:
            c = api('GET', '/component/' + str(matches[0]['id']))
            action = 'existing'
            if c.get('assigneeType') != 'PROJECT_LEAD':
                action = 'updated' if args.apply else 'would_update'
                if args.apply:
                    api('PUT', '/component/' + str(c['id']), {'assigneeType': 'PROJECT_LEAD'})
        elif args.apply:
            c = api('POST', '/component', payload)
            action = 'created'
        else:
            c = payload
            action = 'would_create'
        if args.apply:
            c = api('GET', '/component/' + str(c['id']))
            assert normalized(c['name']) == normalized(name) and c.get('assigneeType') == 'PROJECT_LEAD'
            assert c.get('isAssigneeTypeValid') is not False, f'Project lead cannot be assigned: {name}'
        print(json.dumps({'kind': 'component', 'action': action, 'data': {k: c.get(k) for k in ('id', 'name', 'assigneeType', 'isAssigneeTypeValid')}}, ensure_ascii=False))


if __name__ == '__main__':
    main()
