from collections import defaultdict, deque


class Intcode:
    def __init__(self, program):
        self.program = defaultdict(int, {i: p for i, p in enumerate(program)})
        self.input = deque()
        self.output = []
        self.rb = 0
        self.pos = 0
        self.halt = True
        
        self.modes_values = {
            0: lambda x: self.program[x],
            1: lambda x: x,
            2: lambda x: self.program[x + self.rb],
        }

        self.instructions = {
            1: self.add,
            2: self.mul,
            3: lambda a, _b, _c: self.inp(a),
            4: lambda a, _b, _c: self.out(a),
            5: lambda a, b, _c: self.jump_true(a, b),
            6: lambda a, b, _c: self.jump_false(a, b),
            7: self.less_than,
            8: self.equals,
            9: lambda a, _b, _c: self.adjust_rb(a)
        }

    def is_running(self):
        return not self.halt
    
    def get_modes(self):
        opcode = self.program[self.pos]
        return (opcode%1000//100, opcode%10000//1000, opcode%100000//10000)

    def get_args(self):
        return self.program[self.pos + 1], self.program[self.pos + 2], self.program[self.pos + 3]

    def value(self, a, mode):
        return self.modes_values[mode](a)

    def opcode(self):
        return self.program[self.pos]%100
    
    def add(self, a, b, c):
        mod_a, mod_b, mod_c = self.get_modes()
        if mod_c == 2:
            self.program[c + self.rb] = self.value(a, mod_a) + self.value(b, mod_b)
        else:
            self.program[c] = self.value(a, mod_a) + self.value(b, mod_b)
        self.pos += 4

    def mul(self, a, b, c):
        mod_a, mod_b, mod_c = self.get_modes()
        if mod_c == 2:
            self.program[c + self.rb] = self.value(a, mod_a) * self.value(b, mod_b)
        else:
            self.program[c] = self.value(a, mod_a) * self.value(b, mod_b)
        self.pos += 4

    def inp(self, a):
        if self.get_modes()[0] == 2:
            self.program[a + self.rb] = self.input.popleft()
        else:
            self.program[a] = self.input.popleft()
        self.pos += 2

    def out(self, a):
        self.output.append(self.value(a, self.get_modes()[0]))
        self.pos += 2

    def jump_true(self, a, b):
        mod_a, mod_b, _ = self.get_modes()
        self.pos = self.value(b, mod_b) if self.value(a, mod_a) else self.pos + 3

    def jump_false(self, a, b):
        mod_a, mod_b, _ = self.get_modes()
        self.pos = self.value(b, mod_b) if not self.value(a, mod_a) else self.pos + 3

    def less_than(self, a, b, c):
        mod_a, mod_b, mod_c = self.get_modes()
        if mod_c == 2:
            self.program[c + self.rb] = 1 if self.value(a, mod_a) < self.value(b, mod_b) else 0
        else:
            self.program[c] = 1 if self.value(a, mod_a) < self.value(b, mod_b) else 0
        self.pos += 4

    def equals(self, a, b, c):
        mod_a, mod_b, mod_c = self.get_modes()
        if mod_c == 2:
            self.program[c + self.rb] = 1 if self.value(a, mod_a) == self.value(b, mod_b) else 0
        else:
            self.program[c] = 1 if self.value(a, mod_a) == self.value(b, mod_b) else 0
        self.pos += 4

    def adjust_rb(self, a):
        self.rb += self.value(a, self.get_modes()[0])
        self.pos += 2
    
    def run(self, input=[]):
        self.input = deque(input)
        self.output = []
        while self.opcode()!= 99 and not (self.opcode() == 3 and not self.input):
            self.instructions[self.opcode()](*self.get_args())
        self.halt = self.opcode() == 99
        return self.output
