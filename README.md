# Computer Performance Monitoring Dashboard

A real-time system performance monitoring dashboard built with Python, Flask, and Chart.js. This application tracks CPU, memory, disk, network, and process metrics with a beautiful web-based interface.

## Features

✨ **Real-time Monitoring**
- CPU usage and frequency tracking
- Memory utilization (used, available, total)
- Disk space monitoring
- Network statistics (bytes sent/received, packets)
- Top running processes by memory usage

📊 **Interactive Dashboard**
- Live updating metrics every 5 seconds
- Progress bars for visual representation
- Responsive design (desktop and mobile)
- Color-coded status indicators

🔧 **RESTful API**
- `/api/metrics/current` - Get all current metrics
- `/api/metrics/history` - Get metrics history
- `/api/metrics/cpu` - CPU metrics only
- `/api/metrics/memory` - Memory metrics only
- `/api/metrics/disk` - Disk metrics only
- `/api/metrics/network` - Network metrics only
- `/api/metrics/processes` - Process information

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository
```bash
git clone https://github.com/kamalnathkm/test.git
cd test
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Dashboard

Run the Flask application:
```bash
python dashboard.py
```

The dashboard will be available at: `http://localhost:5000`

### Using the Performance Monitor Directly

```python
from performance_monitor import PerformanceMonitor

# Create monitor instance
monitor = PerformanceMonitor()

# Start monitoring in background
monitor.start_monitoring(interval=5)

# Get current metrics
metrics = monitor.get_current_metrics()
print(metrics)

# Export metrics to JSON
monitor.export_to_json('system_metrics.json')

# Stop monitoring
monitor.stop_monitoring()
```

## Project Structure

```
test/
├── performance_monitor.py   # Core monitoring module
├── dashboard.py             # Flask web server
├── templates/
│   └── dashboard.html       # Web interface
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Performance Metrics Collected

### CPU Metrics
- Usage percentage
- Number of logical/physical cores
- Current frequency (MHz)

### Memory Metrics
- Total, used, and available memory (GB)
- Usage percentage

### Disk Metrics
- Total, used, and free space (GB)
- Usage percentage

### Network Metrics
- Bytes sent and received
- Packets sent and received

### Process Metrics
- Top 5 processes by memory usage
- Process name and memory percentage

## API Response Example

```json
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "cpu": {
    "usage_percent": 25.5,
    "count_logical": 8,
    "count_physical": 4,
    "freq": 2400.0
  },
  "memory": {
    "total_gb": 16.0,
    "used_gb": 8.5,
    "available_gb": 7.5,
    "percent": 53.1
  },
  "disk": {
    "total_gb": 500.0,
    "used_gb": 250.0,
    "free_gb": 250.0,
    "percent": 50.0
  },
  "network": {
    "bytes_sent": 1024000,
    "bytes_recv": 2048000,
    "packets_sent": 10000,
    "packets_recv": 15000
  },
  "processes": [
    {
      "pid": 1234,
      "name": "python.exe",
      "cpu_percent": 5.2,
      "memory_percent": 12.5
    }
  ]
}
```

## Configuration

### Monitor Settings
- **max_history**: Maximum number of metrics to store (default: 100)
- **interval**: Time between metric collection in seconds (default: 5)

Modify these in the source code:
```python
monitor = PerformanceMonitor(max_history=100)
monitor.start_monitoring(interval=5)
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance Considerations

- Memory usage depends on `max_history` setting
- CPU impact is minimal (~1-2% usage)
- Network monitoring includes all system interfaces

## Troubleshooting

### Dashboard not loading
- Check if Flask server is running: `python dashboard.py`
- Verify port 5000 is not in use
- Check browser console for errors (F12)

### Missing metrics
- Some metrics require elevated permissions on Windows
- Run with administrator privileges if needed

### High CPU usage
- Reduce monitoring interval
- Lower `max_history` value
- Close unnecessary processes

## Contributing

Feel free to fork this repository and submit pull requests for any improvements!

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for system monitoring enthusiasts**
