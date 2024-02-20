import heapq

def min_build_time(engines, split_time):
    engine_queue = []

    for engine in engines:
        heapq.heappush(engine_queue, engine)

    while len(engine_queue) > 1:
        fastest_engine = heapq.heappop(engine_queue)
        second_fastest_engine = heapq.heappop(engine_queue)

        heapq.heappush(engine_queue, second_fastest_engine + split_time)

    return heapq.heappop(engine_queue)

if __name__ == "__main__":
    engines = [3,4,5,2]
    split_time = 4

    total_time = min_build_time(engines, split_time)

    print("Minimum time to build all engines:", total_time)
