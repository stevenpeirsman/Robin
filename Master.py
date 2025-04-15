from Listening import listen_for_proximity
from Robot_instruct import say_hello
from Log import log

def main():
    log("Master.py started")
    print("[Master] Waiting for someone to approach...")

    while True:
        distance = listen_for_proximity(threshold=1.0)
        log(f"Proximity trigger met: {distance}m")
        say_hello()
        print("[Master] Greeted user. Waiting again...")
        # Optional cooldown or wait for reset
        break  # remove this if you want to loop forever

if __name__ == "__main__":
    main()