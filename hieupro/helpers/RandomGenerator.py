
import random
import time


class RandomGenerator:
    @staticmethod
    def random_password():
        char_pool = []
        for i in range(26):
            char_pool.append(chr(i + ord('a')))
        for i in range(10):
            char_pool.append(chr(i + ord('0')))
        char_pool.append('#')
        char_pool.append('@')
        char_pool.append('!')
        char_pool.append('&')
        char_pool.append('_')
        char_pool.append('-')
        char_pool.append('*')
        char_pool_len = len(char_pool)

        length = random.randint(6, 20)
        ans = ''
        while length > 0:
            ans += char_pool[random.randint(0, char_pool_len - 1)]
            length -= 1
        return ans

    @staticmethod
    def random_id():
        return str(int(time.time())) + str(random.randint(0, 9999))
