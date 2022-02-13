import os
import string

import yaml


def main():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    for entry in config:
        host, path = f"{entry['url']}/".split("/", 1)
        name_base = name_sanitize(host)
        if path:
            name_base += f"-{name_sanitize(path)}"
        path = path or "/"
        with open(output_path := f"generated/{name_base}-ingress.yaml", "w") as f:
            f.write(make_ingress(host, path, name_base))
        os.system(f"git add \"{output_path}\" >nul 2>&1")
        with open(output_path := f"generated/{name_base}-middleware.yaml", "w") as f:
            f.write(make_middleware(target_file_name(entry["file"]), name_base))
        os.system(f"git add \"{output_path}\" >nul 2>&1")
        copy_file("_static-space.yaml")
        copy_file("_static-nginx.yaml")


def copy_file(name):
    with open(output_path := f"generated/{name}", "w") as f_out:
        with open(name) as f_in:
            f_out.write(f_in.read())
    os.system(f"git add \"{output_path}\" >nul 2>&1")


def target_file_name(name: str):
    assert name is not None
    if not name.startswith("/"):
        name = f"/{name}"
    return name


def name_sanitize(text):
    return "".join(
        char if char in string.ascii_lowercase + string.digits else "-"
        for char
        in text
    )


def expand_file(file_name, info):
    with open(file_name) as f:
        return f.read().format(**info)


def make_ingress(host, path, name):
    return expand_file("base/ingress-base.yaml", locals())


def make_middleware(path, name):
    return expand_file("base/replace-base.yaml", locals())


if __name__ == '__main__':
    main()
