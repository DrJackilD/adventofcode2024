import re
from typing import TypeAlias

INPUT_FILE = "input_24.txt"
GATE = re.compile(r"^(?P<a>\w{3}) (?P<op>AND|OR|XOR) (?P<b>\w{3}) -> (?P<out>\w{3})$")

OPS = {
    "XOR": lambda a, b: a ^ b,
    "AND": lambda a, b: a & b,
    "OR": lambda a, b: a | b,
}

Operation: TypeAlias = tuple[str, str, str, str]


def get_wrong_gates(variables: dict[str, int], operations: set[Operation]) -> str:
    xs, ys = {}, {}

    for v, val in variables.items():
        if v.startswith("x"):
            xs[v] = val
        elif v.startswith("y"):
            ys[v] = val

    ops = {}
    rev_ops = {}

    for op in operations:
        ops[op[3]] = (op[0], op[1], op[2])
        rev_ops[(op[0], op[1], op[2])] = op[3]
        rev_ops[(op[2], op[1], op[0])] = op[3]

    top = max({int(res[1:]) for res in ops if re.match(r"z\d+", res)})

    wrong_gates = set()

    for i in range(1, top):
        x = f"x{i:02d}"
        y = f"y{i:02d}"
        z = f"z{i:02d}"

        res_op = ops[z]

        xor_gate = rev_ops[(x, "XOR", y)]
        and_gate = rev_ops[(x, "AND", y)]

        if "XOR" not in res_op:
            wrong_gates.add(z)

        carry = [
            set(o).difference({"XOR", xor_gate})
            for o in ops.values()
            if "XOR" in o and xor_gate in o
        ]
        if len(carry) != 1:
            wrong_gates.add(xor_gate)
            wrong_gates.add(and_gate)
        else:
            carry = carry[0].pop()
            xor2_gate = rev_ops[(xor_gate, "XOR", carry)]
            if xor2_gate != z:
                wrong_gates.add(xor2_gate)
    return ",".join(sorted(list(wrong_gates)))


def get_number(variables: dict[str, int], ops: set[Operation]) -> int:
    q = [
        gate
        for gate in ops
        if gate[0] in variables and gate[2] in variables and gate[3] not in variables
    ]
    while q:
        for _ in range(len(q)):
            a, op, b, out = q.pop()
            variables[out] = OPS[op](variables[a], variables[b])
        q = [
            gate
            for gate in ops
            if gate[0] in variables
            and gate[2] in variables
            and gate[3] not in variables
        ]

    z = {}
    for v in variables:
        if v.startswith("z"):
            z[int(v[1:])] = variables[v]

    base = "".join(str(z[i]) for i in range(max(z), -1, -1))
    return int(base, 2)


if __name__ == "__main__":
    variables = {}
    gates = []
    with open(INPUT_FILE) as f:
        while line := f.readline().strip():
            var, val = line.split(": ")
            val = int(val)
            variables[var] = val

        while line := f.readline().strip():
            gates.append(GATE.findall(line)[0])

    print(get_number(variables, set(gates)))  # part 1
    print(get_wrong_gates(variables, set(gates)))  # part 2
