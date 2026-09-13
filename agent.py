import time
import logging
import psutil
import urllib3
from urllib3.exceptions import HTTPError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("SentinelAgent")

# Initialize HTTP connection pooler for ntfy / webhooks
http = urllib3.PoolManager(retries=urllib3.Retry(3, redirect=2))

def poll_system_sensors():
    """Safely poll hardware and system telemetry using psutil with error handling."""
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        telemetry = {
            "cpu_percent": cpu_usage,
            "memory_percent": memory.percent,
            "status": "nominal"
        }
        return telemetry
    except Exception as e:
        logger.error(f"Sensor telemetry polling failed: {e}")
        return {"status": "error", "message": str(e)}

def handle_remote_command(command):
    """Process incoming operational commands received via ntfy."""
    cmd = command.strip().upper()
    logger.info(f"Executing remote directive: {cmd}")
    
    if cmd == "STATUS":
        data = poll_system_sensors()
        logger.info(f"Telemetry report generated: {data}")
    elif cmd == "REBOOT":
        logger.warning("Reboot sequence triggered remotely.")
    elif cmd == "STOP":
        logger.warning("Agent stop command received.")
        return False
    else:
        logger.info(f"Unknown or unhandled command: {cmd}")
    return True

def ntfy_listener_loop(topic_url):
    """Poll the ntfy endpoint with robust connection error handling."""
    logger.info(f"Listening for operational triggers on topic: {topic_url}")
    while True:
        try:
            response = http.request('GET', topic_url, timeout=5.0)
            if response.status == 200:
                command = response.data.decode('utf-8')
                if command:
                    active = handle_remote_command(command)
                    if not active:
                        break
        except HTTPError as he:
            logger.warning(f"HTTP communication error with ntfy broker: {he}")
        except Exception as e:
            logger.error(f"Unexpected error in listener loop: {e}")
        
        time.sleep(10)
