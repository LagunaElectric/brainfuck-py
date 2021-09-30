import sys
import math

def pdebug(*stuff) -> None:
    for thing in stuff:
        print(thing, file=sys.stderr, flush=True, end=" ")
    print("", file=sys.stderr, flush=True)

def brackets_match(prog: list[str]) -> bool:
    open_count = 0
    close_count = 0
    for char in prog:
        if char == "[": open_count += 1
        if char == "]": close_count += 1
    return True if open_count == close_count else False

def build_brackmap(code: list[str]) -> dict[int, int]:
    temp_brackmap, brackmap = [], {}

    for pos, char in enumerate(code):
        if char == "[": temp_brackmap.append(pos)
        if char == "]":
            start = temp_brackmap.pop()
            brackmap[start] = pos
            brackmap[pos] = start
    return brackmap

class Pointer:
    def __init__(self, num: int):
        self.val = num

    def inc(self) -> None:
        self.val += 1
        check_value(self.val)

    def dec(self) -> None:
        self.val -= 1
        check_value(self.val)

def check_value(value: int, is_pointer: bool = True) -> None:
    if is_pointer:
        if value < 0 or value > array_size - 1:
            print("POINTER OUT OF BOUNDS")
            exit()
    else:
        if value > 255 or value < 0:
            print("INCORRECT VALUE")
            exit()





# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

line_count, array_size, inputs_count = [int(i) for i in input().split()]

reg: list[int] = [0 for i in range(array_size)]
pdebug(reg)

ptr: Pointer = Pointer(0)

prog_store: list[str] = []

params: list[int] = []

for i in range(line_count):
    for char in list(input()):
        if char in "<>+-.,[]":
            prog_store.append(char)
pdebug(prog_store)
            
if not brackets_match(prog_store):
    print("SYNTAX ERROR")
    exit()

brackmap = build_brackmap(prog_store)
pdebug(brackmap)

for i in range(inputs_count):
    params.append(int(input()))
params.reverse()

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)
i = 0
while i < len(prog_store):
    char = prog_store[i]
    pdebug(f"Char: {char} | Pointer: {ptr.val} | Cell Value: {reg[ptr.val]} | i: {i}")

    if char == ">": ptr.inc()
    if char == "<": ptr.dec()
    if char == ".": print(chr(reg[ptr.val]), end="")

    if char == ",":
        reg[ptr.val] = params.pop()
        check_value(reg[ptr.val], False)
    
    if char == "+":
        reg[ptr.val] += 1
        check_value(reg[ptr.val], False)

    if char == "-":
        reg[ptr.val] -= 1
        check_value(reg[ptr.val], False)

    if char == "[" and reg[ptr.val] == 0:
        i = brackmap[i]

    if char == "]" and reg[ptr.val] != 0:
        i = brackmap[i]
    
    i += 1


