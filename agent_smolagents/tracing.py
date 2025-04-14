import os
import base64
import logging
from typing import Optional, Callable, Any
from dotenv import load_dotenv
import functools
import opentelemetry.trace
from opentelemetry.trace import get_current_span

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Global variables for tracing state
_tracer_provider = None
_tracer = None
IS_TRACING_ENABLED = False

def initialize_otel_tracing() -> bool:
    """
    Initialize OpenTelemetry tracing for smolagents using Langfuse exporter.
    
    Returns:
        bool: True if initialization was successful, False otherwise
    """
    global _tracer_provider, _tracer, IS_TRACING_ENABLED

    LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")

    if not LANGFUSE_PUBLIC_KEY or not LANGFUSE_SECRET_KEY:
        logger.warning("Langfuse API keys not found. OpenTelemetry tracing disabled.")
        IS_TRACING_ENABLED = False
        return False

    try:
        # Import necessary OTel components
        from opentelemetry.sdk.trace import TracerProvider
        from openinference.instrumentation.smolagents import SmolagentsInstrumentor
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor

        logger.info("Configuring Langfuse OpenTelemetry Exporter...")
        LANGFUSE_AUTH = base64.b64encode(
            f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}".encode()
        ).decode()
        
        otel_endpoint = os.getenv(
            "LANGFUSE_HOST_OTEL",
            "https://cloud.langfuse.com/api/public/otel"
        )
        
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = otel_endpoint
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

        # Initialize and configure tracer provider
        _tracer_provider = TracerProvider()
        span_processor = SimpleSpanProcessor(OTLPSpanExporter())
        _tracer_provider.add_span_processor(span_processor)

        # Set global tracer provider
        opentelemetry.trace.set_tracer_provider(_tracer_provider)
        _tracer = opentelemetry.trace.get_tracer("smolagent.request")

        # Instrument smolagents
        SmolagentsInstrumentor().instrument(tracer_provider=_tracer_provider)
        logger.info(f"SmolagentsInstrumentor initialized successfully. Sending traces to: {otel_endpoint}")
        
        IS_TRACING_ENABLED = True
        return True

    except ImportError as e:
        logger.error(
            "OpenTelemetry or SmolagentsInstrumentor dependencies not found. "
            "Langfuse OTel tracing disabled. "
            "Install: pip install opentelemetry-sdk opentelemetry-exporter-otlp openinference-instrumentation-smolagents"
        )
        IS_TRACING_ENABLED = False
        return False
    except Exception as e:
        logger.error(f"Error initializing Langfuse OpenTelemetry: {e}", exc_info=True)
        IS_TRACING_ENABLED = False
        return False

def traced_handler(fn: Callable) -> Callable:
    """
    Decorator to wrap a function call in an OTel span.
    
    Args:
        fn: Function to be traced
        
    Returns:
        Callable: Wrapped function with tracing
    """
    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if not IS_TRACING_ENABLED or not _tracer:
            return fn(*args, **kwargs)

        with _tracer.start_as_current_span("user_request") as span:
            try:
                trace_id = get_current_span().get_span_context().trace_id
                logger.debug(f"Started trace ID: {trace_id:x}")
            except Exception:
                logger.debug("Could not get current trace ID.")

            try:
                result = fn(*args, **kwargs)
                return result
            except Exception as e:
                span.record_exception(e)
                span.set_status(
                    opentelemetry.trace.Status(
                        opentelemetry.trace.StatusCode.ERROR,
                        str(e)
                    )
                )
                raise
    return wrapper
