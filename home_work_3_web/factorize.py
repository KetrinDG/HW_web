from time import time
from multiprocessing import cpu_count, Pool


def factorize(*args) -> dict:
    put_dict = {}
    for i in args:
        division_args = []
        min_count = 1

        while min_count <= i:
            if i % min_count == 0:
                division_args.append(min_count)
                min_count += 1
            else:
                min_count += 1

        put_dict[i] = division_args

    return put_dict


if __name__ == "__main__":
    processors = cpu_count()
    t1 = time()
    result_1 = factorize(128, 255, 99999, 10651060)
    print(f"\033[036mLead time linearly: {time() - t1}\033[0m")
    print(f"\033[033mResult is: {result_1}\033[0m")
    t2 = time()
    pool = Pool(processors)
    result_2 = pool.apply_async(factorize, (128, 255, 99999, 10651060))
    print(f"\033[036mLead time on {processors} processors {time() - t2}\033[0m")
    print(f"\033[033mResult is: {result_2.get()}\033[0m")
