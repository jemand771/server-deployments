import yaml


# pip install pyyaml


def main():
    with open("cert_config.yaml") as f:
        certs_data = [make_cert_data(cert) for cert in yaml.safe_load(f)]
    for data in certs_data:
        for file_name in ("cert", "issuer"):
            input_path = f"base/{file_name}.yaml"
            output_path = f"generated/{data.get('name')}-{file_name}.yaml"
            with open(input_path) as original_file:
                with open(output_path, "w") as out_file:
                    out_file.write(original_file.read().format(**data))
    with open("base/dummy-loader-deploy.yaml") as f_deploy:
        with open("generated/dummy-traefik-cert-loader.yaml", "w") as f:
            f.write(f_deploy.read() + build_ingress(certs_data))


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


def build_ingress(certs_data):
    with open("base/dummy-loader-rule.yaml") as f:
        rule_template = f.read()
    with open("base/dummy-loader-tls.yaml") as f:
        tls_template = f.read()
    return """
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: dummy-traefik-cert-loader
spec:
  rules:
""" + "\n".join(
        rule_template.format(**data) for data in certs_data
    ) + """
  tls:
""" + "\n".join(
        tls_template.format(**data) for data in certs_data
    ) + "\n"


if __name__ == '__main__':
    main()
