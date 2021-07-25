from multiprocessing import Process
from time import sleep
import uvicorn

# global process variable
proc = None


def run_admin(): 
    """
    This function to run admin uvicorn server.
    """
    uvicorn.run(app="main:app_admin", port=8000, reload=True)

def run_ca_admin(): 
    """
    This function to run admin uvicorn server.
    """
    uvicorn.run(app="main:app_ca_admin", port=8000, reload=True)

def run_app(): 
    """
    This function to run app uvicorn server.
    """
    uvicorn.run(app="main:app_app", port=5555, reload=True)

def run_node(): 
    """
    This function to run node uvicorn server.
    """
    uvicorn.run(app="main:app_node", port=5551, reload=True)

def run_ca_node(): 
    """
    This function to run node uvicorn server.
    """
    uvicorn.run(app="main:app_ca_node", port=5551, reload=True)


def start(function):
    """
    This function to start a new process (start the server).
    """
    global proc
    # create process instance and set the target to run function.
    # use daemon mode to stop the process whenever the program stopped.
    proc = Process(target=function, args=())
    proc.start()


def stop(): 
    """
    This function to join (stop) the process (stop the server).
    """
    global proc
    # check if the process is not None
    if proc: 
        # join (stop) the process with a timeout setten to 0.25 seconds.
        # using timeout (the optional arg) is too important in order to
        # enforce the server to stop.
        proc.join(0.25)

if __name__ == "__main__":
    # to start the server call start function.
    # start(run_admin)
    start(run_ca_admin)
    # start(run_app)
    # start(run_node)
    start(run_ca_node)
    # run some codes ....
    # to stop the server call stop function.
    stop()