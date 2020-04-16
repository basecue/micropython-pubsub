from micropython import schedule


def _callback(arg):
    subscriber, args, kwargs = arg
    subscriber(*args, **kwargs)


class PubSub:
    def __init__(self) -> None:
        self._subscribers = {}

    def publish(self, name, *args, **kwargs) -> None:
        try:
            subscribers = self._subscribers[name]
        except KeyError:
            return

        for subscriber in subscribers:
            schedule(_callback, (subscriber, args, kwargs))

    def subscribe(self, name, subscriber) -> None:
        self._subscribers.setdefault(name, []).append(subscriber)
        return subscriber
