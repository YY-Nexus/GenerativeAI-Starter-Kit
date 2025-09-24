import pkg_resources

EXPECTED = {
    "torch": "2.0.1",
    "transformers": "4.32.0",
    "sentence-transformers": "2.2.2",
    "langchain": "0.3.26",
}


def check_versions():
    for pkg, expected in EXPECTED.items():
        try:
            installed = pkg_resources.get_distribution(pkg).version
            assert installed == expected, f"{pkg}: expected {expected}, got {installed}"
        except Exception as e:
            print(f"❌ {pkg} version mismatch: {e}")
        else:
            print(f"✅ {pkg} version OK: {expected}")


if __name__ == "__main__":
    check_versions()
