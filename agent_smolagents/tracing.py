import os
import base64
import logging
from dotenv import load_dotenv
import functools # Needed for decorator
import opentelemetry.trace # Needed for OTel tracer and span
from opentelemetry.trace import get_current_span # For optional trace_id printing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Optional: Load .env file if you store keys there
load_dotenv()

# --- Global variables for tracing state ---
_tracer_provider = None
_tracer = None
IS_TRACING_ENABLED = False # Default to False
# --- End Global variables ---

def initialize_otel_tracing():
    """
    Initializes OpenTelemetry tracing for smolagents using Langfuse exporter.
    Sets module-level flags and tracer upon success.
    Returns True if initialization was successful, False otherwise.
    """
    global _tracer_provider, _tracer, IS_TRACING_ENABLED # Indicate modification

    LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")

    if not LANGFUSE_PUBLIC_KEY or not LANGFUSE_SECRET_KEY:
        logger.warning("Langfuse API keys not found. OpenTelemetry tracing disabled.")
        IS_TRACING_ENABLED = False
        return False

    try:
        # Import necessary OTel components inside the function
        # to avoid import errors if dependencies are missing and tracing is disabled.
        from opentelemetry.sdk.trace import TracerProvider
        from openinference.instrumentation.smolagents import SmolagentsInstrumentor
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor

        logger.info("Configuring Langfuse OpenTelemetry Exporter...")
        LANGFUSE_AUTH = base64.b64encode(f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}".encode()).decode()
        # Choose the correct endpoint based on your Langfuse region (cloud.langfuse.com is EU)
        otel_endpoint = os.getenv("LANGFUSE_HOST_OTEL", "https://cloud.langfuse.com/api/public/otel")
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = otel_endpoint
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

        # Initialize and store the TracerProvider
        _tracer_provider = TracerProvider()
        span_processor = SimpleSpanProcessor(OTLPSpanExporter())
        _tracer_provider.add_span_processor(span_processor)

        # Set the global tracer provider for OTel API
        opentelemetry.trace.set_tracer_provider(_tracer_provider)

        # Get and store the tracer instance
        _tracer = opentelemetry.trace.get_tracer("smolagent.request") # Use the name here

        # Instrument smolagents
        SmolagentsInstrumentor().instrument(tracer_provider=_tracer_provider)
        logger.info(f"SmolagentsInstrumentor initialized successfully. Sending traces to: {otel_endpoint}")
        IS_TRACING_ENABLED = True # Set flag on success
        return True

    except ImportError:
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

# --- Define the Tracing Decorator ---
def traced_handler(fn):
    """Decorator to wrap a function call in an OTel span."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Use the module-level flag and tracer
        if not IS_TRACING_ENABLED or not _tracer:
            return fn(*args, **kwargs)

        # Start the root span for the user request
        with _tracer.start_as_current_span("user_request") as span:
            try:
                trace_id = get_current_span().get_span_context().trace_id
                logger.debug(f"🔍 Started trace ID: {trace_id:x}") # Use logger.debug
            except Exception:
                 logger.debug("🔍 Could not get current trace ID.")

            try:
                result = fn(*args, **kwargs)
                return result
            except Exception as e:
                span.record_exception(e)
                span.set_status(opentelemetry.trace.Status(opentelemetry.trace.StatusCode.ERROR, str(e)))
                raise
    return wrapper
# --- End Tracing Decorator ---
