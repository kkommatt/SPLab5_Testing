from Parser.yacc_grammar import parser
from AST.ast import draw_ast


def main():
    i = 0
    try:
        with open('test.txt', 'r') as file:
            for line in file:
                s = line.strip()
                if not s:
                    continue
                i += 1

                print(f"Expression {i}: {s}")

                result = parser.parse(s)
                print(f"Result: {round(result, 2)}")

                # graph = draw_ast(s)
                # graph.render(f'Output/output_{i}', view=True)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()