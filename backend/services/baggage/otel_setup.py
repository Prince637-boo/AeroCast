from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.aio_pika import AioPikaInstrumentor


def init_tracing(app, db_engine=None):
    resource = Resource.create({"service.name": "baggage-service"})

    provider = TracerProvider(resource=resource)
    otlp_exporter = OTLPSpanExporter(
        # endpoint="http://jaeger:4318/v1/traces"
        endpoint="http://localhost:4318/v1/traces"
    )
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    trace.set_tracer_provider(provider)

    # instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    # instrument SQLAlchemy si fourni
    if db_engine:
        SQLAlchemyInstrumentor().instrument(engine=db_engine.sync_engine)

    # instrument AioPika pour RabbitMQ
    AioPikaInstrumentor().instrument()
