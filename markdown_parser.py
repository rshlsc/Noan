import re

def parse(content, mode):
    if mode == 'anki_front_back':
        bullet_pattern = r'^- (.*?)$'
        sub_bullet_pattern = r'^\s{4}- (.*?)$'
        bullets = re.findall(bullet_pattern, content, re.MULTILINE)
        sub_bullets = re.findall(sub_bullet_pattern, content, re.MULTILINE)
        return list(zip(bullets, sub_bullets))

    elif mode == 'anki_cloze':
        cloze_pattern = r'([^.\n]+(\[.*?\]|\(.*?\))[^.\n]*\.)'
        clozes = re.findall(cloze_pattern, content)
        return [match[0] for match in clozes]
