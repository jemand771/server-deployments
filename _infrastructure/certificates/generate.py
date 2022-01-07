from pathlib import Path

import yaml
# pip install pyyaml


def main():
    with open("cert_config.yaml") as f:
        for cert in yaml.safe_load(f):
            data = make_cert_data(cert)
            for file_path in Path("base").glob("*.yaml"):
                output_path = Path("generated") / f"{data.get('name')}-{file_path.name}"
                with open(file_path) as original_file:
                    with open(output_path, "w") as out_file:
                        out_file.write(original_file.read().format(**data))


def make_cert_data(cert):
    zone = cert.get("name")
    dns_names = cert.get("dns_names", [])
    if cert.get("wildcard", True):
        dns_names.append(f"*.{zone}")
    return {
        "zone": zone,
        "name": zone.replace(".", "-"),
        "dns_names": format_dns_names(dns_names)
    }


def format_dns_names(names):
    assert len(names) > 0
    return "\n".join(f"    - \"{name}\"" for name in names)


if __name__ == '__main__':
    main()
