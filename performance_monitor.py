import psutil
import time
import json
from datetime import datetime
from collections import deque
import threading

class PerformanceMonitor:
    """Monitor computer performance metrics in real-time"""
    
    def __init__(self, max_history=100):
        self.max_history = max_history
        self.metrics_history = deque(maxlen=max_history)
        self.is_running = False
        self.monitor_thread = None
        
    def get_cpu_info(self):
        """Get CPU usage information"""
        return {
            'usage_percent': psutil.cpu_percent(interval=1),
            'count_logical': psutil.cpu_count(logical=True),
            'count_physical': psutil.cpu_count(logical=False),
            'freq': psutil.cpu_freq().current if psutil.cpu_freq() else 0
        }
    
    def get_memory_info(self):
        """Get memory usage information"""
        memory = psutil.virtual_memory()
        return {
            'total_gb': memory.total / (1024**3),
            'used_gb': memory.used / (1024**3),
            'available_gb': memory.available / (1024**3),
            'percent': memory.percent
        }
    
    def get_disk_info(self):
        """Get disk usage information"""
        disk = psutil.disk_usage('/')
        return {
            'total_gb': disk.total / (1024**3),
            'used_gb': disk.used / (1024**3),
            'free_gb': disk.free / (1024**3),
            'percent': disk.percent
        }
    
    def get_network_info(self):
        """Get network statistics"""
        net_io = psutil.net_io_counters()
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv
        }
    
    def get_process_info(self):
        """Get top processes by CPU and Memory"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by memory usage
        top_processes = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:5]
        return top_processes
    
    def collect_metrics(self):
        """Collect all system metrics"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'disk': self.get_disk_info(),
            'network': self.get_network_info(),
            'processes': self.get_process_info()
        }
        self.metrics_history.append(metrics)
        return metrics
    
    def start_monitoring(self, interval=5):
        """Start continuous monitoring in background"""
        self.is_running = True
        
        def monitor_loop():
            while self.is_running:
                try:
                    self.collect_metrics()
                    time.sleep(interval)
                except Exception as e:
                    print(f"Error in monitoring: {e}")
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join()
    
    def get_current_metrics(self):
        """Get latest metrics"""
        if self.metrics_history:
            return self.metrics_history[-1]
        return self.collect_metrics()
    
    def get_metrics_history(self):
        """Get all collected metrics"""
        return list(self.metrics_history)
    
    def export_to_json(self, filename='metrics.json'):
        """Export metrics history to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.get_metrics_history(), f, indent=2)
        return filename


if __name__ == "__main__":
    monitor = PerformanceMonitor()
    
    # Start monitoring
    print("Starting performance monitoring...")
    monitor.start_monitoring(interval=2)
    
    # Collect data for 30 seconds
    try:
        for i in range(15):
            metrics = monitor.get_current_metrics()
            print(f"\n--- Sample {i+1} at {metrics['timestamp']} ---")
            print(f"CPU Usage: {metrics['cpu']['usage_percent']}%")
            print(f"Memory: {metrics['memory']['used_gb']:.2f}GB / {metrics['memory']['total_gb']:.2f}GB ({metrics['memory']['percent']}%)")
            print(f"Disk: {metrics['disk']['used_gb']:.2f}GB / {metrics['disk']['total_gb']:.2f}GB ({metrics['disk']['percent']}%)")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
    finally:
        monitor.stop_monitoring()
        monitor.export_to_json()
        print("Metrics exported to metrics.json")
