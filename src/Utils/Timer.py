import time


class Timer:
    def __init__(self):
        self.reset()

    def reset(self):
        self.time_start = time.time()

    def get_time(self):

        time_end = time.time()
        self.time_elapsed = time_end - self.time_start
        return self.time_elapsed

    def show_time(self, caption="Temps d'exécution : {0}"):
        print(caption.format((f"{self.get_time():.4}s")))


if __name__ == "__main__":
    timer = Timer()
    time.sleep(1)
    timer.show_time(caption="hello {0}")
