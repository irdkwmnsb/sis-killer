import sys
import random

CARD = '''
<div class="card">
    <div class="bg"></div>
    <div class="cardRow killer">
        <div class="name">{k_fname} {k_lname}</div>
        <div class="group">{k_group}</div>
    </div>
    <div class="cardRow yourTarget">Твоя цель</div>
    <div class="cardRow target">
        <div class="name">{t_fname} {t_lname}</div>
        <div class="group">{t_group}</div>
    </div>
</div>
'''

ROW = '''
<div class="row">
{imgs}
</div>'''

N_IN_ROW = 5
N_IN_COLUMN = 14
# 40mm - w,20.5mm - h

PREP_SUFFIX = ".преп"


# 701 - killer-1
# 702 - killer-2
# 703 - killer-prep
COLOR = "blue"
SEED = 703


def get_card(**kwargs):
    return CARD.format(**kwargs)


def get_row(cards):
    return ROW.format(imgs="".join(cards))


def read_template():
    with open("template.html", "r") as f:
        template = f.read()
        template = template \
            .replace("{{N_IN_ROW}}", str(N_IN_ROW)) \
            .replace("{{N_IN_COLUMN}}", str(N_IN_COLUMN)) \
            .replace("{{COLOR}}", COLOR)
        split = template.split("{{CARDS}}")
        assert len(split) == 2
        return split


TEMPLATE_HEAD, TEMPLATE_TAIL = read_template()

import pathlib


def should_find(path: pathlib.Path):
    return path.is_dir() and not path.name.startswith(".")


def make_chain(seed, players: list):
    rnd = random.Random(seed)
    players = players.copy()
    while True:
        rnd.shuffle(players)
        chain = []
        for i in range(len(players)):
            t = (i + 1) % len(players)
            k_group = players[i][2].strip()
            t_group = players[t][2].strip()
            if t_group.endswith(PREP_SUFFIX) and t_group[:-len(PREP_SUFFIX)] == k_group:
                print(f"Fail {k_group} kills {t_group}")
                break
            chain.append({
                "k_fname": players[i][0].strip(),
                "k_lname": players[i][1].strip(),
                "k_group": k_group,
                "t_fname": players[t][0].strip(),
                "t_lname": players[t][1].strip(),
                "t_group": t_group,
            })
        else:
            i = 0
            for e in chain:
                print(f"{e['k_fname']} {e['k_lname']} {e['k_group']} -> {e['t_fname']} {e['t_lname']} {e['t_group']}")
            return chain


def main():
    if len(sys.argv) < 2:
        dir = max(filter(should_find, pathlib.Path.cwd().iterdir()), key=lambda x: x.stat().st_mtime)
    else:
        dir = pathlib.Path(sys.argv[1])
    print("Using dir", dir)
    if (input("Continue? [Y/n] ") or "y").lower() != "y":
        print("Aborting")
        return
    with open(dir / "list.csv", "r") as f:
        players = [line.split(",") for line in f.readlines()]
    chain = make_chain(SEED, players)
    chain.sort(key=lambda x: x["k_group"])
    result_html = dir / "result.html"
    make_cards(chain, result_html)
    print("Done! Result in", result_html)
    pass


def make_cards(cards, result_html):
    with open(result_html, "w") as f:
        f.write(TEMPLATE_HEAD)
        for i in range(0, len(cards), N_IN_ROW):
            f.write(
                get_row(
                    get_card(**card) for card in cards[i:i + N_IN_ROW]
                )
            )
        f.write(TEMPLATE_TAIL)


if __name__ == "__main__":
    main()
