from functions.run_python_file import run_python_file


def test():
    print("Result for running on main.py no args")
    result = run_python_file("calculator", "main.py")
    print(result)
    print("")


    print("Result for running on main.py with args")
    result = run_python_file("calculator", "main.py",["3 + 5"])
    print(result)
    print("")


    print("Result for running on test.py, should run calc test")
    result = run_python_file("calculator", "test.py")
    print(result)
    print("")


    print("Result for running on ../main.py")
    result = run_python_file("calculator", "../main.py")
    print(result)
    print("")


    print("Result for running on nonexistent.py")
    result = run_python_file("calculator", "nonexistent.py")
    print(result)
    print("")


    print("Result for running on lorem.txt")
    result = run_python_file("calculator", "lorem.txt")
    print(result)
    print("")

if __name__ == "__main__":
    test()