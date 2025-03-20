import os
import subprocess
import sys


def _run(*cmd: str, **kwargs) -> None:
    subprocess.run(
        cmd,
        **(
            {
                "stdout": subprocess.DEVNULL,
                "stderr": subprocess.DEVNULL,
            }
            | kwargs
        ),
    )


nix = ["nix", "develop", ".", "-c"] if "USE_NIX" in os.environ else []
clients = (
    lambda u: _run("curl", "-L", u),
    lambda u: _run("firefox", u),
    lambda u: _run("google-chrome-stable", u),
    lambda u: _run(*nix, "go", "run", "gurl.go", u, cwd="go"),
    lambda u: _run(*nix, "java", "Jurl.java", u, cwd="java"),
    lambda u: _run(*nix, "node", ".", u, cwd="node"),
    lambda u: _run(*nix, "cargo", "run", u, cwd="rust"),
    lambda u: _run(*nix, "python3", "purl.py", u, cwd="python"),
)


def main() -> None:
    for u in sys.argv[1:]:
        for c in clients:
            c(u)


if __name__ == "__main__":
    main()
