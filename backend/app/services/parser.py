import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any

from app.models.report_models import TestResultModel


def _text_or_none(node: ET.Element, path: str) -> str:
    target = node.find(path)
    return target.text.strip() if target is not None and target.text else None


def parse_junit_xml(content: str, source: str, pipeline: str, build_number: str, timestamp: datetime) -> List[Dict[str, Any]]:
    tree = ET.fromstring(content)
    records = []
    for suite in tree.findall('.//testsuite'):
        module_name = suite.attrib.get('name')
        for case in suite.findall('testcase'):
            test_name = case.attrib.get('name')
            test_class = case.attrib.get('classname')
            execution_time = float(case.attrib.get('time', 0.0))
            status = 'passed'
            failure = case.find('failure')
            error = case.find('error')
            skipped = case.find('skipped')
            failure_reason = None
            stack_trace = None
            if skipped is not None:
                status = 'skipped'
            elif failure is not None:
                status = 'failed'
                failure_reason = failure.attrib.get('message') or failure.text
                stack_trace = failure.text
            elif error is not None:
                status = 'failed'
                failure_reason = error.attrib.get('message') or error.text
                stack_trace = error.text

            records.append({
                'test_name': test_name,
                'test_class': test_class,
                'module_name': module_name,
                'status': status,
                'execution_time': execution_time,
                'failure_reason': failure_reason,
                'stack_trace': stack_trace,
                'source': source,
                'pipeline': pipeline,
                'build_number': build_number,
                'timestamp': timestamp,
            })
    return records


def parse_allure_xml(content: str, source: str, pipeline: str, build_number: str, timestamp: datetime) -> List[Dict[str, Any]]:
    tree = ET.fromstring(content)
    records = []
    for test_case in tree.findall('.//test-case'):
        test_name = test_case.attrib.get('name')
        test_class = _text_or_none(test_case, 'class-name') or test_case.attrib.get('class')
        module_name = _text_or_none(test_case, 'package')
        status = test_case.attrib.get('status', 'unknown').lower()
        execution_time = float(test_case.attrib.get('time', 0.0))
        failure_reason = _text_or_none(test_case, 'failure/message')
        stack_trace = _text_or_none(test_case, 'failure/stack-trace')
        records.append({
            'test_name': test_name,
            'test_class': test_class,
            'module_name': module_name,
            'status': status,
            'execution_time': execution_time,
            'failure_reason': failure_reason,
            'stack_trace': stack_trace,
            'source': source,
            'pipeline': pipeline,
            'build_number': build_number,
            'timestamp': timestamp,
        })
    return records


def parse_extent_xml(content: str, source: str, pipeline: str, build_number: str, timestamp: datetime) -> List[Dict[str, Any]]:
    tree = ET.fromstring(content)
    records = []
    for test in tree.findall('.//test'):
        test_name = test.attrib.get('name')
        test_class = _text_or_none(test, 'class') or test.attrib.get('class')
        module_name = _text_or_none(test, 'test-category')
        status = test.attrib.get('status', 'unknown').lower()
        execution_time = float(_text_or_none(test, 'duration') or 0.0)
        failure_reason = _text_or_none(test, 'error/message')
        stack_trace = _text_or_none(test, 'error/stackTrace')
        records.append({
            'test_name': test_name,
            'test_class': test_class,
            'module_name': module_name,
            'status': status,
            'execution_time': execution_time,
            'failure_reason': failure_reason,
            'stack_trace': stack_trace,
            'source': source,
            'pipeline': pipeline,
            'build_number': build_number,
            'timestamp': timestamp,
        })
    return records


def parse_report(content: str, report_type: str, source: str, pipeline: str, build_number: str, timestamp: datetime) -> List[Dict[str, Any]]:
    if report_type.lower() == 'junit':
        return parse_junit_xml(content, source, pipeline, build_number, timestamp)
    if report_type.lower() == 'allure':
        return parse_allure_xml(content, source, pipeline, build_number, timestamp)
    if report_type.lower() == 'extent':
        return parse_extent_xml(content, source, pipeline, build_number, timestamp)
    raise ValueError(f'Unsupported report type: {report_type}')
