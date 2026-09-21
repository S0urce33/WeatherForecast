from time import sleep

try:
    from plyer import notification

except ImportError:
    print("Required modules not found. Please install them using 'pip install plyer'")
    sleep(5)
    exit()


notification.notify(
    title="Test",
    message="If you see this, plyer works",
    timeout=10
)