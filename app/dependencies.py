from app.pubsub import PubSub

_pubsub_instance = None

async def get_pubsub() -> PubSub:
    global _pubsub_instance
    if _pubsub_instance is None:
        _pubsub_instance = PubSub()  # create_pubsub ki zarurat nahi
    return _pubsub_instance
