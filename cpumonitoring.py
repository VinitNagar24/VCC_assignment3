import psutil
import time
from googleapiclient.discovery import build
from google.oauth2 import service_account

PROJECT_ID = 'vm01-452603'
ZONE = 'us-central1-a'
INSTANCE_GROUP_NAME = 'web-migration'
MIGRATION_SCRIPT = 'migration_script.sh'  # Script to migrate app

def check_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"Current CPU usage: {cpu_usage}%")
    return cpu_usage

def migrate_application():
    credentials = service_account.Credentials.from_service_account_file('/home/vmfedora/vccAssignment3/service-account-key.json')
    service = build('compute', 'v1', credentials=credentials)

    # Start migration by creating a new VM instance in the managed instance group
    request = service.instanceGroupManagers().resize(
        project=PROJECT_ID,
        zone=ZONE,
        instanceGroupManager=INSTANCE_GROUP_NAME,
        size=2  # Increase size by 1 to scale up
    )
    response = request.execute()
    print(f"Migrating application, scaling group: {response}")

while True:
    cpu_usage = check_cpu_usage()
    if cpu_usage > 75:
        print("CPU usage is high, migrating application to GCP...")
        migrate_application()
    time.sleep(60)  # Check every minute

