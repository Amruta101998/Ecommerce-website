class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            return "Stack is empty"

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return "Stack is empty"

    def size(self):
        return len(self.items)


def evaluate_postfix(expression):
    stack = Stack()
    operators = {'+': lambda x, y: x + y, '-': lambda x, y: x - y, '*': lambda x, y: x * y, '/': lambda x, y: x / y}

    for char in expression.split():
        if char.isdigit():
            stack.push(int(char))
        elif char in operators:
            operand2 = stack.pop()
            operand1 = stack.pop()
            result = operators[char](operand1, operand2)
            stack.push(result)

    return stack.pop()


if __name__ == "__main__":
    postfix_expression = "4 5 * +"
    result = evaluate_postfix(postfix_expression)
    print("Result of evaluating postfix expression {}: {}".format(postfix_expression, result))
