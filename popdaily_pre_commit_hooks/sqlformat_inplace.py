import os
import sys
from subprocess import CalledProcessError, check_output
from typing import Optional, Sequence

from sqlparse import cli as sqlparse_cli


def sqlformat_inplace(args, filename):
    try:
        output_sql = check_output(
            " ".join(["sqlformat", *args, filename]), shell=True
        ).decode("utf-8")
        output_sql += "\n"
    except CalledProcessError as e:
        print(e)
        return e.returncode

    with open(filename) as fp:
        input_sql = fp.read()

    if input_sql != output_sql:
        with open(filename, "w") as fp:
            fp.write(output_sql)
        print(f"{filename}: fixed by sqlparse")
        return 1
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    # allow multiple filenames
    parser = sqlparse_cli.create_parser()
    for action in parser._actions:
        if action.dest == "filename":
            action.nargs = "+"

    # get args and filenames
    args = sys.argv[1:]
    parsed_args = parser.parse_args()

    filenames = parsed_args.filename
    args_without_filenames = [a for a in args if a not in parsed_args.filename]

    # run sqlformat once per file
    result = 0
    for filename in filenames:
        return_value = sqlformat_inplace(args_without_filenames, filename)
        if return_value != 0:
            result = return_value
    return result


if __name__ == "__main__":
    exit(main())
