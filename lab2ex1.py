import argparse
import os

RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
RESET   = "\033[0m"
BOLD    = "\033[1m"

COLOR_MAP = {
    "red": RED,
    "green": GREEN,
    "yellow": YELLOW,
    "blue": BLUE,
    "magenta": MAGENTA,
    "cyan": CYAN,
    "none": ""
}

def read_lines(filepath, num_lines, verbose, line_numbers, color):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = []
        for i in range(num_lines):
            line = f.readline()
            if not line:
                break
            content = line.rstrip()
            if line_numbers:
                content = f"{i+1:>4}: {content}"
            if color:
                content = f"{color}{content}{RESET}"
            lines.append(content)

        if verbose:
            header = f"{BOLD}{color}==> {filepath} <=={RESET}" if color else f"{BOLD}==> {filepath} <=={RESET}"
            print(header)

        print('\n'.join(lines))

def read_bytes(filepath, num_bytes, verbose, color):
    with open(filepath, 'rb') as f:
        data = f.read(num_bytes)
        text = data.decode('utf-8', errors='replace')
        if color:
            text = f"{color}{text}{RESET}"
        if verbose:
            header = f"{BOLD}{color}==> {filepath} <=={RESET}" if color else f"{BOLD}==> {filepath} <=={RESET}"
            print(header)
        print(text)

def main():
    parser = argparse.ArgumentParser(description="Python version of Unix head")
    parser.add_argument("filepath", help="Path to the file")
    parser.add_argument("-n", type=int, help="Number of lines to read", default=None)
    parser.add_argument("-c", type=int, help="Number of bytes to read", default=None)
    parser.add_argument("-v", action="store_true", help="Verbose: show filename header")
    parser.add_argument("--line-numbers", action="store_true", help="Show line numbers")
    parser.add_argument(
    "--color",
    choices=["red", "green", "yellow", "blue", "magenta", "cyan", "none"],
    default="none",
    help="Color for output text and header"
    ) 
    args = parser.parse_args()

    if not os.path.isfile(args.filepath):
        print(f"Error: File '{args.filepath}' not found.")
        return

    chosen_color = COLOR_MAP[args.color]

    if args.c is not None:
        read_bytes(args.filepath, args.c, args.v, chosen_color)
    else:
        num_lines = args.n if args.n is not None else 10
        read_lines(args.filepath, num_lines, args.v, args.line_numbers, chosen_color)

    if args.c is not None:
        read_bytes(args.filepath, args.c, args.v, args.color)
    else:
        num_lines = args.n if args.n is not None else 10
        read_lines(args.filepath, num_lines, args.v, args.line_numbers, args.color)

if __name__ == "__main__":

    main()

