import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, Float, DateTime, Text, MetaData
from app.services.database import database, metadata
from datetime import datetime

report_table = Table(
    'test_reports',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('source', String, nullable=False),
    Column('pipeline', String, nullable=False),
    Column('report_type', String, nullable=False),
    Column('build_number', String, nullable=False),
    Column('timestamp', DateTime, nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow),
)

result_table = Table(
    'test_results',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('report_id', Integer, nullable=False),
    Column('test_name', String, nullable=False),
    Column('test_class', String, nullable=True),
    Column('module_name', String, nullable=True),
    Column('status', String, nullable=False),
    Column('execution_time', Float, nullable=False),
    Column('failure_reason', Text, nullable=True),
    Column('stack_trace', Text, nullable=True),
    Column('build_number', String, nullable=False),
    Column('timestamp', DateTime, nullable=False),
)

failure_patterns_table = Table(
    'failure_patterns',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('reason', Text, nullable=False),
    Column('module_name', String, nullable=True),
    Column('occurrences', Integer, default=0),
    Column('last_seen', DateTime, nullable=True),
)

flaky_tests_table = Table(
    'flaky_tests',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('test_name', String, nullable=False),
    Column('test_class', String, nullable=True),
    Column('module_name', String, nullable=True),
    Column('flaky_score', Float, nullable=False),
    Column('risk_level', String, nullable=False),
    Column('confidence_score', Float, nullable=False),
    Column('last_evaluated', DateTime, nullable=True),
)

recommendations_table = Table(
    'recommendations',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('test_name', String, nullable=False),
    Column('reason', Text, nullable=False),
    Column('recommendation', Text, nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow),
)

quality_digest_table = Table(
    'quality_digests',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('generation_time', DateTime, nullable=False),
    Column('summary', Text, nullable=False),
    Column('html_digest', Text, nullable=False),
    Column('slack_message', Text, nullable=True),
)

async def persist_report_records(records):
    query = report_table.insert().values(
        source=records[0]['source'],
        pipeline=records[0]['pipeline'],
        report_type=records[0]['report_type'],
        build_number=records[0]['build_number'],
        timestamp=records[0]['timestamp'],
    )
    report_id = await database.execute(query)
    inserted = 0
    for record in records:
        result_query = result_table.insert().values(
            report_id=report_id,
            test_name=record['test_name'],
            test_class=record.get('test_class'),
            module_name=record.get('module_name'),
            status=record['status'],
            execution_time=record['execution_time'],
            failure_reason=record.get('failure_reason'),
            stack_trace=record.get('stack_trace'),
            build_number=record['build_number'],
            timestamp=record['timestamp'],
        )
        await database.execute(result_query)
        inserted += 1
    return inserted
