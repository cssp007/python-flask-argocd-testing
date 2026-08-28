from flask import Flask, render_template, Response
from prometheus_client import Counter, Histogram, generate_latest
import time

app = Flask(__name__)

# --------------------------------------------------
# Prometheus Metrics
# --------------------------------------------------

REQUEST_COUNT = Counter(
    "flask_http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "flask_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)


# --------------------------------------------------
# Request Metrics
# --------------------------------------------------

@app.before_request
def before_request():
    # Store request start time
    from flask import request
    request.start_time = time.time()


@app.after_request
def after_request(response):
    from flask import request

    duration = time.time() - request.start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code,
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.path,
    ).observe(duration)

    return response


# --------------------------------------------------
# Application Routes
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")


# --------------------------------------------------
# Prometheus Metrics Endpoint
# --------------------------------------------------

@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype="text/plain",
    )


# --------------------------------------------------
# Application Startup
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )