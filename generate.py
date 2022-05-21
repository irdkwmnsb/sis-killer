IMG = '''
<div class="pic">
<div class="imgcontainer">
<img src="{src}"/>
</div>
<div class="title">{name}</div>
<div class="extra">{extra}</div>
</div>
'''

ROW = '''
<div class="row">
{imgs}
</div>'''

N_IN_ROW = 5
N_IN_COLUMN = 6


def get_img(src, name, extra):
    return IMG.format(src=src, name=name, extra=extra or "")


def get_row(imgs):
    return ROW.format(imgs="".join(imgs))


def read_template():
    with open("template.html", "r") as f:
        template = f.read()
        template = template\
            .replace("{{N_IN_ROW}}", str(N_IN_ROW)) \
            .replace("{{N_IN_COLUMN}}", str(N_IN_COLUMN))
        split = template.split("{{IMAGES}}")
        assert len(split) == 2
        return split


TEMPLATE_HEAD, TEMPLATE_TAIL = read_template()

import pathlib


def should_find(path: pathlib.Path):
    return path.is_dir() and not path.name.startswith(".")


def main():
    dir = max(filter(should_find, pathlib.Path.cwd().iterdir()), key=lambda x: x.stat().st_mtime)
    print("Using dir", dir)
    if (input("Continue? [Y/n] ") or "y").lower() != "y":
        print("Aborting")
        return
    extras = {}
    if (dir / "extra.csv").exists():
        print("Using extras")
        with open(dir / "extra.csv") as f:
            for line in f:
                name, extra = line.split(", ")
                extras[name.strip()] = extra.strip()
    files = list(dir.rglob("*.png"))
    result_html = dir / "result.html"
    with open(result_html, "w") as f:
        f.write(TEMPLATE_HEAD)
        for i in range(0, len(files), N_IN_ROW):
            f.write(
                get_row(
                    get_img(src=file.relative_to(result_html.parent),
                            name=file.stem.strip(),
                            extra=extras.get(file.stem.strip()))
                    for file in files[i:i + N_IN_ROW]
                )
            )
        f.write(TEMPLATE_TAIL)
    print("Done! Result in", result_html)
    pass


if __name__ == "__main__":
    main()
