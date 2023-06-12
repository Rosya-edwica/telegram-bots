from redis import Redis

r = Redis("127.0.0.1", 6379)
minus = [i.decode("utf-8") for i in r.smembers("minus_skill")]
correct = [i.decode("utf-8") for i in r.smembers("correct_skill")]

print(minus)
print(correct)