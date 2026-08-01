import pytest
from datetime import datetime
from backend.app.services.parser import parse_report


def test_parse_junit_xml_success():
    xml = '''<testsuites><testsuite name="module.a"><testcase classname="ClassA" name="test_a" time="1.23"><failure message="Assertion failed">stack</failure></testcase></testsuite></testsuites>'''
    records = parse_report(xml, 'junit', 'github', 'workflow', '123', datetime.utcnow())
    assert len(records) == 1
    assert records[0]['status'] == 'failed'
    assert records[0]['failure_reason'] == 'Assertion failed'


def test_parse_allure_xml_success():
    xml = '''<ns:test-suite xmlns:ns="urn:allure"><test-case name="test_b" status="failed" time="0.5"><class-name>ClassB</class-name><package>module.b</package><failure><message>Error</message><stack-trace>trace</stack-trace></failure></test-case></ns:test-suite>'''
    records = parse_report(xml, 'allure', 'jenkins', 'pipeline', '456', datetime.utcnow())
    assert len(records) == 1
    assert records[0]['module_name'] == 'module.b'
    assert records[0]['status'] == 'failed'


def test_parse_extent_xml_success():
    xml = '''<tests><test name="test_c" status="failed"><class>ClassC</class><test-category>module.c</test-category><duration>2.5</duration><error><message>Error</message><stackTrace>trace</stackTrace></error></test></tests>'''
    records = parse_report(xml, 'extent', 'manual', 'upload', '789', datetime.utcnow())
    assert len(records) == 1
    assert records[0]['status'] == 'failed'
    assert records[0]['execution_time'] == 2.5
