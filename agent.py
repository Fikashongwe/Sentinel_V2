import os
import json
import logging
import psutil
import urllib3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("SentinelAgent")

# Disable insecure request warnings and initialize urllib3 PoolManager
urllib3.disable_warnings()
http = urllib3.PoolManager()

# Load Slack Webhook URL securely from environment variable
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(message):
    """Send operational alerts or telemetry data to Slack via webhook."""
    if not SLACK_WEBHOOK_URL:
        logger.warning("SLACK_WEBHOOK_URL environment variable not set. Skipping Slack alert.")
        return False
    
    try:
        payload = json.dumps({"text": message})
        response = http.request(
            'POST',
            SLACK_WEBHOOK_URL,
            body=payload,
            headers={'Content-Type': 'application/json'}
        )
        if response.status == 200:
            logger.info("Slack alert sent successfully.")
            return True
        else:
            logger.error(f"Failed to send Slack alert. Status code: {response.status}")
            return False
    except Exception as e:
        logger.error(f"Exception occurred while sending Slack alert: {e}")
        return False

def poll_system_sensors():
    """Gather system telemetry metrics like CPU, memory, and battery status."""
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        battery = psutil.sensors_battery()
        
        telemetry = {
            "cpu_percent": cpu_usage,
            "memory_percent": memory.percent,
            "battery_percent": battery.percent if battery else "N/A",
            "power_plugged": battery.power_plugged if battery else "N/A"
        }
        return telemetry
    except Exception as e:
        logger.error(f"Error polling system sensors: {e}")
        return {}

def handle_remote_command(command):
    """Process incoming remote directives."""
    cmd = command.strip().upper()
    logger.info(f"Executing remote directive: {cmd}")
    
    if cmd == "STATUS":
        data = poll_system_sensors()
        msg = f"🛡️ *Sentinel_V2 Status Report*:\n```json\n{json.dumps(data, indent=2)}\n```"
        logger.info(f"Telemetry report generated: {data}")
        send_slack_alert(msg)
    elif cmd == "REBOOT":
        logger.warning("Reboot sequence triggered remotely.")
        send_slack_alert("⚠️ *Sentinel_V2*: Reboot sequence triggered remotely.")
    elif cmd == "STOP":
        logger.warning("Agent stop command received.")
        send_slack_alert("🛑 *Sentinel_V2*: Agent stop command received.")
        return False
    else:
        logger.info(f"Unknown or unhandled command: {cmd}")
    return True

def ntfy_listener_loop(topic_url):
    """Poll the operational endpoint with robust connection error handling."""
    logger.info(f"Listening for operational triggers on topic: {topic_url}")
    while True:
        try:
            response = http.request('GET', topic_url, timeout=5.0)
            if response.status == 200:
                command = response.data.decode('utf-8').strip()
                if command:
                    active = handle_remote_command(command)
                    if not active:
                        break
        except urllib3.exceptions.HTTPError as he:
            logger.error(f"HTTP error during polling: {he}")
        except Exception as e:
            logger.error(f"Error in listener loop: {e}")

if __name__ == "__main__":
    logger.info("Starting Sentinel_V2 Agent...")
    send_slack_alert("🚀 *Sentinel_V2*: Agent initialized and running.")
    
    # Configure your ntfy topic or command source URL via environment variable or default
    ntfy_topic_url = os.getenv("NTFY_TOPIC_URL", "https://ntfy.sh/sentinel_v2_status_demo")
    
    try:
        ntfy_listener_loop(ntfy_topic_url)
    except KeyboardInterrupt:
        logger.info("Agent stopped manually by user.")
        send_slack_alert("🛑 *Sentinel_V2*: Agent stopped manually.")
