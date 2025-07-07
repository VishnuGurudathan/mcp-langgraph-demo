import sys
import json
import traceback

def calculate(operation: str, a: float, b: float) -> float:
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    else:
        raise ValueError(f"Unsupported operation: {operation}")

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break

        try:
            request = json.loads(line)
            args = request.get("arguments", {})
            operation = args.get("operation")
            a = float(args.get("a"))
            b = float(args.get("b"))
            result = calculate(operation, a, b)
            response = {"result": result}
        except Exception as e:
            response = {"error": str(e), "traceback": traceback.format_exc()}

        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
