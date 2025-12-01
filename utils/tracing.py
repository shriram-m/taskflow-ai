import os
from typing import Optional
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor

tracer_provider: Optional[TracerProvider] = None
tracer: Optional[trace.Tracer] = None

def setup_tracing(service_name: str = "taskflow-ai") -> Optional[trace.Tracer]:
    """Initialize OpenTelemetry tracing"""
    global tracer_provider, tracer
    
    try:
        enable = os.getenv("ENABLE_TRACING", "true").lower() == "true"
        if not enable:
            return None
        
        # Use the correct import path for Jaeger exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name=os.getenv("JAEGER_AGENT_HOST", "localhost"),
            agent_port=int(os.getenv("JAEGER_AGENT_PORT", "6831")),
        )
        
        tracer_provider = TracerProvider()
        tracer_provider.add_span_processor(SimpleSpanProcessor(jaeger_exporter))
        trace.set_tracer_provider(tracer_provider)
        
        tracer = trace.get_tracer(__name__)
        
        # Instrument HTTP libraries
        RequestsInstrumentor().instrument()
        URLLib3Instrumentor().instrument()
        
    except Exception as e:
        print(f"Warning: Could not setup tracing: {e}")
    
    return tracer

def get_tracer() -> Optional[trace.Tracer]:
    """Get global tracer instance"""
    return tracer
