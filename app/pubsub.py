import asyncio
import json

class PubSub:
    def __init__(self):
        self.subscribers = []

    async def publish(self, channel, message):
        # Broadcast to all subscribers
        for queue in self.subscribers:
            await queue.put(message)

    async def subscribe(self, channel):
        queue = asyncio.Queue()
        self.subscribers.append(queue)
        try:
            while True:
                message = await queue.get()
                yield message
        finally:
            self.subscribers.remove(queue)

# Global singleton
_pubsub_instance: PubSub | None = None

async def get_pubsub() -> PubSub:
    global _pubsub_instance
    if _pubsub_instance is None:
        _pubsub_instance = PubSub()
    return _pubsub_instance
