from typing import Dict, Type, Any
from textual.screen import Screen

class ScreenRegistry:
    _screens: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def register(cls, name: str, animation_profile: str = "default"):
        def decorator(subclass: Type[Screen]):
            cls._screens[name] = {"class": subclass, "animation": animation_profile}
            return subclass
        return decorator

    @classmethod
    def get_screen(cls, name: str):
        return cls._screens.get(name)

class AnimationManager:
    @staticmethod
    def pulse(widget, attribute: str = "opacity", duration: float = 1.0):
        widget.styles.animate(attribute, 1.0, duration=duration/2, easing="in_out_sine")
        # Textual animations can be chained or used with callbacks
        # For simplicity, we'll implement a helper that can be called

    @staticmethod
    def slide_in(widget, duration: float = 0.5):
        widget.styles.offset = (100, 0)
        widget.styles.animate("offset", (0, 0), duration=duration, easing="out_cubic")

class ResponseMiddleware:
    """Chain of responsibility for LLM responses."""
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    def process(self, text: str) -> str:
        for handler in self.handlers:
            text = handler(text)
        return text
