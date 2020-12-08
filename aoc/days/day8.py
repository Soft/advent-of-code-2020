def instructions(input):
    def parse(line):
        opcode, operand = line.split(" ", 2)
        return opcode, int(operand)

    return [parse(line) for line in input.splitlines()]


def evaluate(instructions):
    executed = [False] * len(instructions)
    acc = 0
    ip = 0
    while True:
        if ip == len(instructions):
            return acc, True
        if executed[ip]:
            return acc, False
        executed[ip] = True
        opcode, operand = instructions[ip]
        if opcode == "acc":
            acc += operand
            ip += 1
        elif opcode == "jmp":
            ip += operand
        elif opcode == "nop":
            ip += 1
        else:
            assert False


def part_1(input):
    acc, _ = evaluate(instructions(input))
    print(acc)


def generate_variants(instructions):
    yield instructions
    for i, (opcode, operand) in enumerate(instructions):
        if opcode == "jmp":
            instruction = "nop", operand
        elif opcode == "nop":
            instruction = "jmp", operand
        else:
            continue
        yield instructions[:i] + [instruction] + instructions[i + 1 :]


def part_2(input):
    for program in generate_variants(instructions(input)):
        acc, ok = evaluate(program)
        if ok:
            print(acc)
            break
