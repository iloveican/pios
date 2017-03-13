import random


numbers = [l.split() for l in """
一 二 三 四 五 六 七 八 九 十
① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ 
""".strip().splitlines()]


def get_tiles(size):
    assert not self.size % 2
    game = random.sample(list(range(len(numbers[0]))), size // 2)
    tiles = sum(([(i, numbers[0][i]), (i, numbers[1][i])] for i in game), [])
    random.shuffle(tiles)
    return tiles
