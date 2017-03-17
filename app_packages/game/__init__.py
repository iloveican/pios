import random


numbers = [l.split() for l in """
一 二 三 四 五 六 七 八 九 十
① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩
""".strip().splitlines()]


operators = "eq ne ge le gt lt pw ls tu st".split(), "== != => <= > < ** [] () {}".split()


def get_tiles(size):
    assert not size % 2
    source = random.choice((numbers, operators))
    game = random.sample(list(range(len(source[0]))), size // 2)
    tiles = sum(([(i, source[0][i]), (i, source[1][i])] for i in game), [])
    random.shuffle(tiles)
    return tiles
