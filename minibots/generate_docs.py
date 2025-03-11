def generate_readme():
    with open('README.md', 'w') as readme:
        readme.write("# ScraperBot\n\n")
        readme.write("## Setup Instructions\n")
        readme.write("1. Install Python, Git, and VS Code.\n")
        readme.write("2. Set up the virtual environment and install dependencies.\n")
        readme.write("3. Configure the `.env` file with your Discord bot token.\n")
        readme.write("4. Run the bot using `python import_discord1.py`.\n")
        readme.write("\n## Features\n")
        readme.write("- Message parsing and deal extraction.\n")
        readme.write("- User interactivity and command handling.\n")
        readme.write("- Automated forwarding and category management.\n")
        readme.write("- Advanced AI features for deal prioritization.\n")

def generate_changelog():
    with open('Changelog.md', 'w') as changelog:
        changelog.write("# Changelog\n\n")
        changelog.write("## [Unreleased]\n")
        changelog.write("- Initial release.\n")

if __name__ == "__main__":
    generate_readme()
    generate_changelog()
