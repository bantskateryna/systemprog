import argparse
import os

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"
BOLD = "\033[1m"

def uniq(filepath, count=False, duplicates=False, unique_only=False, verbose=False, color=False):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = [line.rstrip('\n') for line in f]

    output = []
    prev = None
    freq = 0

    for line in lines + [None]:
        if line == prev:
            freq += 1
        else:
            if prev is not None:
                show = True
                if duplicates and freq < 2:
                    show = False
                if unique_only and freq > 1:
                    show = False
                if show:
                    if count:
                        prefix = f"{YELLOW}{freq:>4}{RESET} " if color else f"{freq:>4} "
                        output.append(f"{prefix}{prev}")
                    else:
                        output.append(prev)
            prev = line
            freq = 1

    if verbose:
        header = f"{BOLD}{CYAN}==> {filepath} <=={RESET}" if color else f"\033[1m==> {filepath} <==\033[0m"
        print(header)

    print('\n'.join(output))

def main():
    parser = argparse.ArgumentParser(description="Python version of Unix uniq")
    parser.add_argument("filepath", help="Path to the file")
    parser.add_argument("-c", action="store_true", help="Prefix lines by the number of occurrences")
    parser.add_argument("-d", action="store_true", help="Only print duplicate lines")
    parser.add_argument("-u", action="store_true", help="Only print unique lines")
    parser.add_argument("-v", action="store_true", help="Verbose: show filename header")
    parser.add_argument("--color", action="store_true", help="Enable colored output")
    args = parser.parse_args()

    if not os.path.isfile(args.filepath):
        print(f"Error: File '{args.filepath}' not found.")
        return

    uniq(args.filepath, args.c, args.d, args.u, args.v, args.color)

if __name__ == "__main__":
    main()