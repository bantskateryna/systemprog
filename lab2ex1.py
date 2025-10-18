import argparse
import os

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"
BOLD = "\033[1m"
def read_lines(filepath, num_lines, verbose, line_numbers, color):
    with open(filepath, 'r', encoding='utf-8',) as f:
        lines = []
        for i in range(num_lines):
            line = f.readline()
            if not line:
                break
            if line_numbers:
                lines.append(f"{i+1:>4}: {line.rstrip()}")
            else:
                lines.append(line.rstrip())
        if verbose:
            header = f"{BOLD}{CYAN}==> {filepath} <=={RESET}" if color else f"\033[1m==> {filepath} <==\033[0m"
            print(header)

        print('\n'.join(lines))

def read_bytes(filepath, num_bytes, verbose, color):
    with open(filepath, 'rb') as f:
        data = f.read(num_bytes)
        if verbose:
            header = f"{BOLD}{MAGENTA}  {filepath}{RESET}" if color else f"\033[1m==> {filepath} <==\033[0m"
            print(header)
        print(data.decode('utf-8'))

def main():
    parser = argparse.ArgumentParser(description="Python version of Unix head")
    parser.add_argument("filepath", help="Path to the file")
    parser.add_argument("-n", type=int, help="Number of lines to read", default=None)
    parser.add_argument("-c", type=int, help="Number of bytes to read", default=None)
    parser.add_argument("-v", action="store_true", help="Verbose: show filename header")
    parser.add_argument("--line-numbers", action="store_true", help="Show line numbers")
    parser.add_argument("--color", action="store_true", help="Enable colored output")
    args = parser.parse_args()

    if not os.path.isfile(args.filepath):
        print(f"Error: File '{args.filepath}' not found.")
        return

    if args.c is not None:
        read_bytes(args.filepath, args.c, args.v, args.color)
    else:
        num_lines = args.n if args.n is not None else 10
        read_lines(args.filepath, num_lines, args.v, args.line_numbers, args.color)

if __name__ == "__main__":
    main()