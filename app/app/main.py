import logging
import uvicorn
from fastapi import FastAPI
from app.config import app_config
from app.core.fastapi.routers import health

app = FastAPI()

# Observability — only loaded when OBSERVABILITY=true
if app_config.observability_enabled:
    from app.core.otlp.utils import PrometheusMiddleware, metrics, setting_otlp, EndpointFilter
    app.add_middleware(PrometheusMiddleware, app_name=app_config.app_name)
    app.add_route("/metrics", metrics)

# include routers
app.include_router(health.router)

if app_config.observability_enabled:
    setting_otlp(app, app_config.app_name, app_config.otlp_grpc_endpoint)
    logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
def start():
    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    if app_config.observability_enabled:
        log_config["formatters"]["access"]["fmt"] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    else:
        log_config["formatters"]["access"]["fmt"] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
    # uvicorn.run(app, host="0.0.0.0", port=int(app_config.port), log_config=log_config, timeout_keep_alive=0)

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(app_config.port),
        log_config=log_config,
        workers=2,  # Adjust the number of workers based on your server's capabilities
        reload=False,  # Enable auto-reload during development
        timeout_keep_alive=0
    )

if __name__ == "__main__":
    start()