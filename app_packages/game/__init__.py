import random


numbers = [l.split() for l in """
一 二 三 四 五 六 七 八 九 十
① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩
""".strip().splitlines()]

braille = [l.split() for l in """
⠼⠚ ⠼⠁ ⠼⠃ ⠼⠉ ⠼⠙ ⠼⠑ ⠼⠋ ⠼⠛ ⠼⠓ ⠼⠊
⓪ ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨
""".strip().splitlines()]

images = [l.split() for l in """
cat dog owl beach wave tree cup school
😸 🐶 🦉 🏖 🌊 🌲 🍵 🏫
""".strip().splitlines()]

flags = [l.split() for l in """
singapore malaysia usa finland japan korea italy china
🇸🇬 🇲🇾 🇺🇸 🇫🇮 🇯🇵 🇰🇷 🇮🇹 🇨🇳
""".strip().splitlines()]


def get_tiles(size):
    assert not size % 2
    source = random.choice((flags,))
    game = random.sample(list(range(len(source[0]))), size // 2)
    tiles = sum(([(i, source[0][i]), (i, source[1][i])] for i in game), [])
    random.shuffle(tiles)
    return tiles
