from flask import Flask, render_template, jsonify
from flask_cors import CORS
from performance_monitor import PerformanceMonitor
import threading
import json

app = Flask(__name__)
CORS(app)

# Initialize performance monitor
monitor = PerformanceMonitor()
monitor.start_monitoring(interval=5)

@app.route('/')
def index():
    """Render dashboard home page"""
    return render_template('dashboard.html')

@app.route('/api/metrics/current')
def get_current_metrics():
    """Get current system metrics"""
    try:
        metrics = monitor.get_current_metrics()
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics/history')
def get_metrics_history():
    """Get metrics history"""
    try:
        history = monitor.get_metrics_history()
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics/cpu')
def get_cpu_metrics():
    """Get CPU metrics"""
    try:
        metrics = monitor.get_current_metrics()
        return jsonify(metrics['cpu'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics/memory')
def get_memory_metrics():
    """Get memory metrics"""
    try:
        metrics = monitor.get_current_metrics()
        return jsonify(metrics['memory'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics/disk')
def get_disk_metrics():
    """Get disk metrics"""
    try:
        metrics = monitor.get_current_metrics()
        return jsonify(metrics['disk'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics/processes')
def get_process_metrics():
    """Get process metrics"""
    try:
        metrics = monitor.get_current_metrics()
        return jsonify(metrics['processes'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics/network')
def get_network_metrics():
    """Get network metrics"""
    try:
        metrics = monitor.get_current_metrics()
        return jsonify(metrics['network'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
