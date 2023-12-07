from src.cli.cli_handler import CLIHandler

if __name__ == "__main__":
    args = CLIHandler.parseCLI()
    cli_handler = CLIHandler(args)  # Create an instance of CLIHandler
    cli_handler.handle_task()  # Call the handle_task method