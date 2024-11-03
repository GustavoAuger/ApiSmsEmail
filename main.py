from api1.app import app as api1_app
from api2.app import app as api2_app
from threading import Thread

def run_api1():
    api1_app.run(port=5000)

def run_api2():
    api2_app.run(port=5001)

if __name__ == "__main__":
    Thread(target=run_api2).start()
    Thread(target=run_api1).start()