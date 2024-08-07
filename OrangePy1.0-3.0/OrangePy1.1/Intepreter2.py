import ast


RED = "\033[31m"
RESET = "\033[0m"

class OrangePy:
    def __init__(self):
        self.variables = {}

    def run(self):
        while True:
            try:
                localinput = input(">> ")
                self.parse(localinput)
            except KeyboardInterrupt:
                print("\nExiting...")
                break

    def parse(self, command):
        command = command.strip()
        if command.lower().startswith("print "):
            self.println(command[6:])
        elif command.lower().startswith("var "):
            self.assign(command[4:])
        elif command.lower().startswith("if "):
            self.condition(command[3:])
        elif command.lower().startswith("  "):
            self.condition(command[2:])           
        else:
            print(f"{RED}SyntaxError: Invalid syntax{RESET}")

    def println(self, value):
        value = value.strip()
        if value in self.variables:
            value = self.variables[value]
        print(value)

    def cin(self, var_name):
        var_name = var_name.strip()
        if not var_name.isidentifier():
            print(f"{RED}VariableError: Invalid variable name{RESET}")
            return
        user_input = input(f"{var_name} ")
        self.variables[var_name] = user_input

    def assign(self, statement):
        if "=" in statement:
            var_name, value = statement.split("=", 1)
            var_name = var_name.strip()
            value = value.strip()
            if value.lower() == "input":
                self.cin(var_name)
            else:
                if any(op in value for op in "+-*/"):
                    value = self.bmaths(value)
                elif value.isdigit():
                    value = int(value)
                elif value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]  # Remove surrounding quotes
                elif value in self.variables:
                    value = self.variables[value]
                self.variables[var_name] = value
        else:
            print(f"{RED}VariableError: Invalid assignment statement{RESET}")

    def condition(self, statement):
        if " then " in statement:
            condition, action = statement.split(" then ", 1)
            condition = condition.strip()
            action = action.strip()
            if self.evaluate_condition(condition):
                self.parse(action)
        else:
            print(f"{RED}SyntaxError: Invalid if statement format{RESET}")

    def evaluate_condition(self, condition):
        try:
            for var_name in self.variables:
                condition = condition.replace(var_name, str(self.variables[var_name]))
            return eval(condition)
        except Exception as e:
            print(f"{RED}Error evaluating condition: {e}{RESET}")
            return False

    def bmaths(self, expr):
        try:
            for var_name in self.variables:
                expr = expr.replace(var_name, str(self.variables[var_name]))
            tree = ast.parse(expr, mode='eval')
            compiled = compile(tree, filename="<string>", mode="eval")
            return eval(compiled)
        except Exception as e:
            print(f"{RED}Error evaluating expression: {e}{RESET}")
            return None












