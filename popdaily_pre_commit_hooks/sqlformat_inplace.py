import os
import sys
from subprocess import CalledProcessError, check_output
from typing import Optional, Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = sys.argv[1:]
    input_path = args[-1]

    try:
        output_sql = check_output(" ".join(["sqlformat", *args]), shell=True).decode(
            "utf-8"
        )
        output_sql += "\n"
    except CalledProcessError as e:
        print(e)
        return e.returncode

    with open(input_path) as fp:
        input_sql = fp.read()

    if input_sql != output_sql:
        with open(input_path, "w") as fp:
            fp.write(output_sql)
        print(f"{input_path}: fixed by sqlparse")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
