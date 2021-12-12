import sys


def pdebug(*stuff) -> None:
    for thing in stuff:
        print(thing, file=sys.stderr, flush=True, end=" ")
    print("", file=sys.stderr, flush=True)


def brackets_match(prog: list[str]) -> bool:
    open_count = 0
    close_count = 0
    for char in prog:
        if char == "[":
            open_count += 1
        if char == "]":
            close_count += 1
    return True if open_count == close_count else False


def build_brackmap(code: list[str]) -> dict[int, int]:
    temp_brackmap, brackmap = [], {}

    for pos, char in enumerate(code):
        if char == "[":
            temp_brackmap.append(pos)
        if char == "]":
            start = temp_brackmap.pop()
            brackmap[start] = pos
            brackmap[pos] = start
    return brackmap


class Pointer:
    def __init__(self, num: int, array_size: int):
        self.val = num
        self.array_size = array_size

    def inc(self) -> None:
        self.val += 1
        check_value(self.array_size, self.val)

    def dec(self) -> None:
        self.val -= 1
        check_value(self.array_size, self.val)


def check_value(arr_size: int, value: int, is_pointer: bool = True) -> None:
    if is_pointer:
        if value < 0 or value > arr_size:
            print("POINTER OUT OF BOUNDS")
            exit()
    else:
        if value > 255 or value < 0:
            print("INCORRECT VALUE")
            exit()


def main(array_size: int, bf_prog: list[str], params: list[int]):
    reg: list[int] = [0 for i in range(array_size)]

    ptr: Pointer = Pointer(0, array_size)

    prog_store: list[str] = []

    params: list[int] = []

    with open(bf_prog, 'r') as program:
        for line in program:
            for char in line:
                if char in "<>+-.,[]":
                    prog_store.append(char)

    if not brackets_match(prog_store):
        print("SYNTAX ERROR")
        exit()

    brackmap = build_brackmap(prog_store)
    print(brackmap)

    params = params.reverse()

    i = 0
    while i < len(prog_store):
        char = prog_store[i]
        # pdebug(f"Char: {char} | Pointer: {ptr.val} | Cell Value: {reg[ptr.val]} | i: {i}")

        if char == ">":
            ptr.inc()
        if char == "<":
            ptr.dec()
        if char == ".":
            print(chr(reg[ptr.val]), end="")

        if char == ",":
            reg[ptr.val] = params.pop()
            check_value(array_size, reg[ptr.val], False)

        if char == "+":
            reg[ptr.val] += 1
            check_value(array_size, reg[ptr.val], False)

        if char == "-":
            reg[ptr.val] -= 1
            check_value(array_size, reg[ptr.val], False)

        if char == "[" and reg[ptr.val] == 0:
            i = brackmap[i]

        if char == "]" and reg[ptr.val] != 0:
            i = brackmap[i]

        i += 1


if __name__ == '__main__':
    args = sys.argv[1:3]
    args_to_pass = args[2:]

    print(len(args))
    print(args)

    if len(args) < 2:
        print("Must give 2+ args. line_count: int, array_size: int, inputs_count: int, filename: str, input1: int, input2: int, input3: int...")
        exit()

    with open(args[1], 'r') as bf_file:
        lines = bf_file.readlines()

    for i in range(len(args)):
        if i != 1:
            try:
                test = int(args[i])
            except ValueError:
                print(f"Arg {i + 1} must be an int.")
                exit()

    for i in range(len(args_to_pass)):
        try:
            args_to_pass[i] = int(args_to_pass[i])
        except ValueError:
            print(f"Arg {i + 1} must be an int.")
            exit()

    array_size = int(args[0])
    print(f"arr size before main is {array_size}")
    filename = args[1]

    main(array_size, filename, args_to_pass)
