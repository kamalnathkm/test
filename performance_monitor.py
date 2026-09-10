import psutil
import time
import json
from datetime import datetime
from collections import deque
import threading
import traceback

class PerformanceMonitor:
    """Monitor computer performance metrics in real-time"""
    
    def __init__(self, max_history=100):
        self.max_history = max_history
        self.metrics_history = deque(maxlen=max_history)
        self.is_running = False
        self.monitor_thread = None
        
    def get_cpu_info(self):
        """Get CPU usage information"""
        try:
            freq = psutil.cpu_freq()
            return {
                'usage_percent': round(psutil.cpu_percent(interval=0.1), 2),
                'count_logical': psutil.cpu_count(logical=True),
                'count_physical': psutil.cpu_count(logical=False),
                'freq': round(freq.current, 2) if freq else 0
            }
        except Exception as e:
            return {
                'usage_percent': 0,
                'count_logical': 0,
                'count_physical': 0,
                'freq': 0
            }
    
    def get_memory_info(self):
        """Get memory usage information"""
        try:
            memory = psutil.virtual_memory()
            return {
                'total_gb': round(memory.total / (1024**3), 2),
                'used_gb': round(memory.used / (1024**3), 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'percent': round(memory.percent, 2)
            }
        except Exception as e:
            return {
                'total_gb': 0,
                'used_gb': 0,
                'available_gb': 0,
                'percent': 0
            }
    
    def get_disk_info(self):
        """Get disk usage information"""
        try:
            disk = psutil.disk_usage('/')
            return {
                'total_gb': round(disk.total / (1024**3), 2),
                'used_gb': round(disk.used / (1024**3), 2),
                'free_gb': round(disk.free / (1024**3), 2),
                'percent': round(disk.percent, 2)
            }
        except Exception as e:
            return {
                'total_gb': 0,
                'used_gb': 0,
                'free_gb': 0,
                'percent': 0
            }
    
    def get_network_info(self):
        """Get network statistics"""
        try:
            net_io = psutil.net_io_counters()
            return {
                'bytes_sent': int(net_io.bytes_sent),
                'bytes_recv': int(net_io.bytes_recv),
                'packets_sent': int(net_io.packets_sent),
                'packets_recv': int(net_io.packets_recv)
            }
        except Exception as e:
            return {
                'bytes_sent': 0,
                'bytes_recv': 0,
                'packets_sent': 0,
                'packets_recv': 0
            }
    
    def get_process_info(self):
        """Get top processes by CPU and Memory"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info
                    pid = info.get('pid', 0)
                    name = info.get('name', 'Unknown')
                    
                    # Ensure name is a valid string
                    if name and isinstance(name, str):
                        name = name[:50]  # Limit name length
                    else:
                        name = 'Unknown'
                    
                    cpu_pct = info.get('cpu_percent')
                    mem_pct = info.get('memory_percent')
                    
                    # Convert to float and round
                    try:
                        cpu_pct = round(float(cpu_pct) if cpu_pct else 0, 2)
                        mem_pct = round(float(mem_pct) if mem_pct else 0, 2)
                    except (ValueError, TypeError):
                        cpu_pct = 0.0
                        mem_pct = 0.0
                    
                    processes.append({
                        'pid': int(pid),
                        'name': name,
                        'cpu_percent': cpu_pct,
                        'memory_percent': mem_pct
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError, TypeError, AttributeError):
                    pass
            
            # Sort by memory usage
            top_processes = sorted(processes, key=lambda x: x.get('memory_percent', 0), reverse=True)[:5]
            return top_processes
        except Exception as e:
            return []
    
    def collect_metrics(self):
        """Collect all system metrics"""
        try:
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
        except Exception as e:
            print(f"Error collecting metrics: {e}")
            return None
    
    def start_monitoring(self, interval=5):
        """Start continuous monitoring in background"""
        self.is_running = True
        
        def monitor_loop():
            while self.is_running:
                try:
                    self.collect_metrics()
                    time.sleep(interval)
                except Exception as e:
                    pass  # Silently continue monitoring
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.is_running = False
        if self.monitor_thread:
            try:
                self.monitor_thread.join(timeout=2)
            except:
                pass
    
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
        try:
            with open(filename, 'w') as f:
                json.dump(self.get_metrics_history(), f, indent=2)
            return filename
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return None


if __name__ == "__main__":
    monitor = PerformanceMonitor()
    
    # Start monitoring
    print("Starting performance monitoring...")
    monitor.start_monitoring(interval=2)
    
    # Collect data for 30 seconds
    try:
        for i in range(15):
            metrics = monitor.get_current_metrics()
            if metrics:
                print(f"\n--- Sample {i+1} at {metrics['timestamp']} ---")
                print(f"CPU Usage: {metrics['cpu']['usage_percent']}%")
                print(f"Memory: {metrics['memory']['used_gb']}GB / {metrics['memory']['total_gb']}GB ({metrics['memory']['percent']}%)")
                print(f"Disk: {metrics['disk']['used_gb']}GB / {metrics['disk']['total_gb']}GB ({metrics['disk']['percent']}%)")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
    finally:
        monitor.stop_monitoring()
        monitor.export_to_json()
        print("Metrics exported to metrics.json")
