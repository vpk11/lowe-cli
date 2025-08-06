import argparse
from dotenv import load_dotenv
from services.lowe_cli import LoweCli

INTRO_MSG: str = """
Welcome to LoweCLI!
This tool is designed to assist developers by providing an interactive command-line assistant that can answer questions, generate code, and help with various programming tasks. Just type your query and let LoweCLI help you boost your productivity!
"""

def main() -> None:
    load_dotenv()
    
    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog='lowe-cli', description='AI powered command-line tool')
    parser.add_argument('-d', '--docs', help='Look up docs')
    parser.add_argument('-p', '--perform', help='execute user command')
    parser.add_argument('-l', '--lookup', help='Look up for a specific document')
    args: argparse.Namespace = parser.parse_args()
    if args.docs:
        LoweCli.help(args.docs)
    elif args.perform:
        LoweCli.perform(args.perform)
    elif args.lookup:
        LoweCli.index()
        LoweCli.lookup(args.lookup)
    else:
        print(INTRO_MSG)
        LoweCli.ask()

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")
    main()
