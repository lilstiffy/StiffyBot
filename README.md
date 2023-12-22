
## Getting Started

1. **Clone this repository:**

    ```bash
    git clone https://github.com/lilstiffy/StiffyBot.git
    ```

2. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your Discord bot token:**

    - Create a new Discord bot on the [Discord Developer Portal](https://discord.com/developers/applications).
    - Copy the token and add it to a file named `.env` in the project root:

    ```env
    DISCORD_TOKEN=your-bot-token (required)
    OPEN_AI_TOKEN=your-open-ai-token (optional)
    URBAN_DICTIONARY_TOKEN=your-urban-dictionary-token (optional)
    ```
   An Urban dictionary api-key can be retrieved at: https://rapidapi.com/community/api/urban-dictionary

4. **Run the bot:**

    ```bash
    python bot.py
    ```

    Your bot should now be online and ready to respond to commands in your Discord server!

## Contributing

If you'd like to contribute to this project, feel free to do so! 

## License

This project is licensed under the Unlicense License - see the [LICENSE](LICENSE) file for details.
