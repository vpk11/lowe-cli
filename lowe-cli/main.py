import signal
import argparse
import sys
from dotenv import load_dotenv
from services.lowe_cli import LoweCli

INTRO_MSG = """
Welcome to LoweCLI!
This tool is designed to assist developers by providing an interactive command-line assistant that can answer questions, generate code, and help with various programming tasks. Just type your query and let LoweCLI help you boost your productivity!
"""

def handle_exit(_signum, _frame):
    print("\nbye bye")
    sys.exit(0)

def main():
    load_dotenv()
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    
    parser = argparse.ArgumentParser(prog='lowe-cli',description='AI powered command-line tool')
    parser.add_argument('-d', '--docs', help='Look up docs')
    parser.add_argument('-p', '--perform', help='execute user command')
    parser.add_argument('-l', '--lookup', help='Look up for a specific document')
    args = parser.parse_args()
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
