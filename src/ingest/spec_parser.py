def parse_endpoints(spec):
    endpoints = []
    paths = spec.get("paths", {})
    for path, methods in paths.items():
        for method, detail in methods.items():
            params = detail.get("parameters", [])
            endpoints.append({
                "method": method.upper(),
                "path": path,
                "params": [p.get("name") for p in params]
            })
    return endpoints
