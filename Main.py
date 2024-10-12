import discord
from discord.ext import commands
from discord.ext import tasks

### Variables -- you can change it for yourself or add smth

TOKEN = ""  # Copy your user token (tutorial: https://www.youtube.com/watch?v=DTFXUfzbmWE)

Timeout = 15

Channel1 = 1234
Channel2 = 4567
Channel3 = 7890

Channels = {
    "Channel1": {"timeout": Timeout, "id": Channel1},
    "Channel2": {"timeout": Timeout, "id": Channel2},
    "Channel3": {"timeout": Timeout, "id": Channel3}
}

Text = "It's a sample text!"  # Change it to your text
image_path = r""  # Change this variable if you have any photo you want to send with the file.

Client = commands.Bot(command_prefix='!', self_bot=True, intents=all)

### Functions

async def Send_message(channel, timeout_value, img_path):

    @tasks.loop(seconds=timeout_value)
    async def Send():
        try:
            if img_path != "":
                with open(img_path, 'rb') as file:
                    picture = discord.File(file)
                    await channel.send(Text, file=picture)
            else:
                await channel.send(Text)
            print(f"Message sent to channel {channel}")
        except discord.errors.HTTPException as e:
            print(f"Failed to send message to channel {channel}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred in channel {channel}: {e}")

    Send.start()  # Start the task loop


async def ChannelFunc(img_path):
    for channel_name, properties in Channels.items():
        timeout_value = properties["timeout"]
        channel_id = properties["id"]

        channel = Client.get_channel(channel_id)
        if channel is None:
            print(f"Channel with ID {channel_id} not found or bot lacks access.")
            return
        else:
            await Send_message(channel, timeout_value, img_path)


async def main():
    await ChannelFunc(image_path)


@Client.event
async def on_ready():
    await main()

Client.run(TOKEN)
