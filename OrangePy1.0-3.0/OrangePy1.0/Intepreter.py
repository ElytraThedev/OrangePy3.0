RED = "\033[31m"
RESET = "\033[0m"

class OrangePy:
    def __init__(self):
        self.variables = {}

    def run(self):
        while True:
            try:
                # Get user input
                localinput = input(">> ")
                self.parse(localinput)
            except KeyboardInterrupt:
                print("\nExiting...")
                break

    def parse(self, command):
        # Basic command parsing
        if command.startswith("PRINT "):
            self.println(command[6:])
        elif command.startswith("INPUT "):
            self.cin(command[6:])
        elif command.startswith("LET "):
            self.assign(command[4:])
        else:
            print(f"{RED}SyntaxError: Invalid syntax{RESET}")        

    def println(self, value):
        # Print the value
        value = value.strip()
        if value in self.variables:
            value = self.variables[value]
        print(value)

    def cin(self, var_name):
        # Read input and store it in a variable
        var_name = var_name.strip()
        if not var_name.isidentifier():
            print(f"{RED}VariableError: Invalid variable name{RESET}")
            return
        user_input = input(f"{var_name} ")
        self.variables[var_name] = user_input

    def assign(self, statement):
        # Handle variable assignment
        if "=" in statement:
            var_name, value = statement.split("=", 1)
            var_name = var_name.strip()
            value = value.strip()
            if any(op in value for op in "+-*/"):
                value = self.bmaths(value)
            elif value.isdigit():
                value = int(value)
            elif value in self.variables:
                value = self.variables[value]
            self.variables[var_name] = value
        else:
            print(f"{RED}VariableError: Invalid assignment statement{RESET}")

    def bmaths(self, expr):
        try:
            # Replace variable names in the expression with their values
            for var_name in self.variables:
                expr = expr.replace(var_name, str(self.variables[var_name]))
            return eval(expr)
        except Exception as e:
            print(f"{RED}Error evaluating expression: {e}{RESET}")
            return None





