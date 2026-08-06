import sys


def parse_tasks(filename):
    tasks = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                e, p, d = [float(x) for x in line.split(',')]
                tasks.append((e, p, d))
    return tasks


def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    filename = sys.argv[1]
    tasks = parse_tasks(filename)


if __name__ == "__main__":
    main()

