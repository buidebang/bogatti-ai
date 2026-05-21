from textual.app import App, ComposeResult
from textual.screen import Screen, ModalScreen
from textual.widgets import Header, Footer, Static, Input, Log, Markdown, Button, Label, TabbedContent, TabPane
from textual.containers import Container, Horizontal, Vertical, Grid, ScrollableContainer
from textual.binding import Binding
from textual import on
from credits_manager import CreditManager
from ai_service import AIService
from schemas import ModelInfo, ConfigInfo, PersonaInfo
from pydantic import TypeAdapter
from typing import List
import json
import asyncio
import os
import re
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display

from engine import ScreenRegistry, AnimationManager, ResponseMiddleware
from compiler import ContentCompiler, BlackboardCanvas

def fix_persian(text):
    if not text:
        return ""
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

class ChatMessage(Static):
    """A widget for a single chat message."""
    def __init__(self, text: str, sender: str, middleware: ResponseMiddleware = None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        if middleware:
            self.text = middleware.process(text)
        self.sender = sender
        self.compiler = ContentCompiler()

    def compose(self) -> ComposeResult:
        if self.sender == "user":
            yield Static(f"[bold blue]You:[/]\n{fix_persian(self.text)}", classes="message user-message")
        else:
            if "$$" in self.text or (self.text.count("$") >= 2):
                yield BlackboardCanvas(self.text, classes="message ai-message")
            else:
                yield Markdown(fix_persian(self.text), classes="message ai-message")

@ScreenRegistry.register("admin_login")
class AdminLoginScreen(ModalScreen):
    def __init__(self, secret: str, **kwargs):
        super().__init__(**kwargs)
        self.secret = secret

    def compose(self) -> ComposeResult:
        with Vertical(id="login-panel"):
            yield Label("Enter Admin Secret Key:")
            yield Input(password=True, id="secret-input")
            with Horizontal():
                yield Button("Login", variant="success", id="login-btn")
                yield Button("Cancel", variant="error", id="cancel-btn")

    @on(Button.Pressed, "#login-btn")
    @on(Input.Submitted, "#secret-input")
    def check_secret(self):
        entered = self.query_one("#secret-input", Input).value
        if entered == self.secret:
            self.dismiss(True)
        else:
            self.app.notify("Invalid Secret Key!", severity="error")

    @on(Button.Pressed, "#cancel-btn")
    def cancel(self):
        self.dismiss(False)

@ScreenRegistry.register("otp_auth")
class OTPAuthScreen(ModalScreen):
    """Iranian SMS OTP Authentication Screen."""
    def compose(self) -> ComposeResult:
        with Vertical(id="otp-panel"):
            yield Label(fix_persian("ورود با شماره موبایل (SMS OTP)"))
            yield Input(placeholder="09123456789", id="phone-input")
            yield Button(fix_persian("ارسال کد تایید"), variant="primary", id="send-otp")
            yield Input(placeholder=fix_persian("کد تایید"), id="otp-input", visible=False)
            yield Button(fix_persian("تایید نهایی"), variant="success", id="verify-otp", visible=False)
            yield Button(fix_persian("انصراف"), variant="error", id="cancel-otp")

    @on(Button.Pressed, "#send-otp")
    async def send_otp(self):
        phone = self.query_one("#phone-input", Input).value
        if re.match(r"^09\d{9}$", phone):
            self.notify(fix_persian(f"کد تایید به شماره {phone} ارسال شد (شبیه‌سازی)."))
            self.query_one("#phone-input").disabled = True
            self.query_one("#send-otp").visible = False
            self.query_one("#otp-input").visible = True
            self.query_one("#verify-otp").visible = True
        else:
            self.notify(fix_persian("شماره موبایل نامعتبر است."), severity="error")

    @on(Button.Pressed, "#verify-otp")
    def verify_otp(self):
        otp = self.query_one("#otp-input", Input).value
        if len(otp) == 4:
            self.dismiss(True)
        else:
            self.notify(fix_persian("کد تایید اشتباه است."), severity="error")

    @on(Button.Pressed, "#cancel-otp")
    def cancel(self):
        self.dismiss(False)

@ScreenRegistry.register("admin_panel")
class AdminScreen(Screen):
    def __init__(self, config: dict, models: list, **kwargs):
        super().__init__(**kwargs)
        self.app_config = config
        self.models_data = models

    def compose(self) -> ComposeResult:
        with Vertical(id="admin-panel"):
            yield Label("Admin Dashboard", id="admin-title")
            with TabbedContent():
                with TabPane("Pricing & Rates"):
                    yield Label("Toman per USD Rate:")
                    yield Input(str(self.app_config["rates"]["toman_per_usd"]), id="rate-input")
                    yield Label("Model Pricing (USD):")
                    with ScrollableContainer():
                        for model in self.models_data:
                            input_id = f"price-{model['display_name'].replace(' ', '_').replace('.', '_')}"
                            yield Horizontal(
                                Label(model["display_name"], classes="model-label"),
                                Input(str(model["cost_per_request"]), id=input_id),
                                classes="price-row"
                            )
                with TabPane("Strings"):
                    with ScrollableContainer():
                        for key, value in self.app_config["strings"].items():
                            yield Label(f"{key}:")
                            yield Input(value, id=f"str-{key}")
                with TabPane("Personas"):
                    with ScrollableContainer():
                        for key, persona in self.app_config["personas"].items():
                            yield Label(f"Persona: {key}")
                            yield Label("System Prompt:")
                            yield Input(persona["system_prompt"], id=f"persona-prompt-{key}")

            yield Horizontal(
                Button("Save", variant="success", id="save-admin"),
                Button("Close", variant="error", id="close-admin"),
                classes="admin-actions"
            )

    @on(Button.Pressed, "#save-admin")
    def save_settings(self):
        try:
            self.app_config["rates"]["toman_per_usd"] = int(self.query_one("#rate-input", Input).value)
            for model in self.models_data:
                input_id = f"#price-{model['display_name'].replace(' ', '_').replace('.', '_')}"
                model["cost_per_request"] = float(self.query_one(input_id, Input).value)
            for key in self.app_config["strings"]:
                self.app_config["strings"][key] = self.query_one(f"#str-{key}", Input).value
            for key in self.app_config["personas"]:
                self.app_config["personas"][key]["system_prompt"] = self.query_one(f"#persona-prompt-{key}", Input).value
            ConfigInfo(**self.app_config)
            TypeAdapter(List[ModelInfo]).validate_python(self.models_data)
            with open("config.json", "w") as f:
                json.dump(self.app_config, f, indent=2, ensure_ascii=False)
            with open("models.json", "w") as f:
                json.dump(self.models_data, f, indent=2, ensure_ascii=False)
            self.app.notify("Settings saved!")
            self.app.pop_screen()
        except Exception as e:
            self.app.notify(f"Error saving settings: {e}", severity="error")

    @on(Button.Pressed, "#close-admin")
    def close_admin(self):
        self.app.pop_screen()

class BalanceWidget(Static):
    def on_mount(self):
        self.update_balance("0.00")
    def update_balance(self, balance: str):
        self.update(f"Balance: [bold green]${balance}[/]")

class BugattiApp(App):
    CSS = """
    Screen { background: #1e1e2e; }
    .message { padding: 1 2; margin: 1; }
    .user-message { background: #313244; color: #cdd6f4; text-align: right; }
    .ai-message { background: #45475a; color: #f5e0dc; }
    .model-item { padding: 0 1; margin: 0 1; }
    .model-active { background: #89b4fa; color: #11111b; }
    #loading-bar { width: 100%; height: 1; background: #313244; color: #fab387; visibility: hidden; }
    #loading-bar.active { visibility: visible; }
    #admin-panel, #otp-panel, #login-panel { background: #11111b; border: double #89b4fa; padding: 2; margin: 2 4; }
    #login-panel, #otp-panel { width: 50; height: auto; align: center middle; }
    #admin-title { text-align: center; color: #89b4fa; margin-bottom: 1; }
    .price-row { height: auto; }
    .model-label { width: 1fr; }
    #app-grid { layout: grid; grid-size: 2; grid-columns: 1fr 25; grid-rows: 3 1fr 3; }
    #chat-log { height: 1fr; overflow-y: scroll; }
    Header { column-span: 2; background: #313244; color: #cdd6f4; }
    BalanceWidget { text-align: right; padding: 1 2; color: #89b4fa; }
    #chat-container { background: #181825; border: solid #45475a; margin: 1; layout: vertical; }
    #sidebar { background: #11111b; border: solid #45475a; margin: 1; }
    #input-container { column-span: 2; padding: 0 1; }
    Input { background: #313244; border: none; }
    .admin-actions { margin-top: 1; align: center middle; }
    """
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("a", "toggle_admin", "Admin", show=True),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.credit_manager = CreditManager()
        self.ai_service = AIService()
        self.load_config()
        self.is_authenticated = False
        self.guest_queries = 0
        self.middleware = ResponseMiddleware()
        # Add a dummy middleware for illustration
        self.middleware.add_handler(lambda x: x)
        os.makedirs("history", exist_ok=True)

    def load_config(self):
        with open("config.json", "r") as f:
            data = json.load(f)
            self.config = ConfigInfo(**data).model_dump()
        with open("models.json", "r") as f:
            models_data = json.load(f)
            self.models = TypeAdapter(List[ModelInfo]).validate_python(models_data)
            self.models = [m.model_dump() for m in self.models]
        self.current_model = self.models[0]
        self.current_persona = self.config["personas"]["developer"]
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.history_file = f"history/chat_{self.session_id}.json"
        self.chat_history = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="app-grid"):
            yield Static(fix_persian(self.config["strings"]["app_title"]), id="title")
            yield BalanceWidget(id="balance")
            with Vertical(id="chat-container"):
                yield Vertical(id="chat-log")
                yield Static("Thinking...", id="loading-bar")
            with Vertical(id="sidebar"):
                yield Static("Models", id="models-title")
                for model in self.models:
                    model_id = f"model-{model['display_name'].replace(' ', '_').replace('.', '_')}"
                    yield Button(f"{model['icon']} {model['display_name']}", classes="model-item", id=model_id)
            with Horizontal(id="input-container"):
                yield Input(placeholder=self.config["strings"]["input_placeholder"], id="chat-input")
        yield Footer()

    def on_mount(self):
        self.query_one(BalanceWidget).update_balance(self.credit_manager.get_balance_usd_str())
        self._update_model_ui()

    def _update_model_ui(self):
        for model in self.models:
            model_id = f"#model-{model['display_name'].replace(' ', '_').replace('.', '_')}"
            widget = self.query_one(model_id, Button)
            if model == self.current_model:
                widget.add_class("model-active")
            else:
                widget.remove_class("model-active")

    @on(Button.Pressed, ".model-item")
    def handle_model_click(self, event: Button.Pressed):
        model_name_safe = event.button.id.replace("model-", "")
        for model in self.models:
            if model['display_name'].replace(' ', '_').replace('.', '_') == model_name_safe:
                self.current_model = model
                self._update_model_ui()
                self.notify(fix_persian(self.config["strings"]["model_switched"].format(model=model['display_name'])))
                break

    def _save_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.chat_history, f, indent=2, ensure_ascii=False)

    @on(Input.Submitted, "#chat-input")
    async def handle_submit(self, event: Input.Submitted):
        if not self.is_authenticated and self.guest_queries >= 1:
            def after_otp(success):
                if success:
                    self.is_authenticated = True
                    self.notify("Authentication successful!")
            await self.push_screen(OTPAuthScreen(), after_otp)
            return

        text = event.value.strip()
        if not text: return
        self.query_one("#chat-input", Input).value = ""

        cost = self.current_model["cost_per_request"]
        if self.credit_manager.balance_usd < cost:
            self.notify(fix_persian(self.config["strings"]["error_low_balance"]), severity="error")
            return

        chat_log = self.query_one("#chat-log", Vertical)
        await chat_log.mount(ChatMessage(text, "user"))
        chat_log.scroll_end()
        self.chat_history.append({"sender": "user", "text": text, "timestamp": str(datetime.now())})

        self.credit_manager.deduct_usd(cost)
        self.query_one(BalanceWidget).update_balance(self.credit_manager.get_balance_usd_str())

        loading_bar = self.query_one("#loading-bar", Static)
        loading_bar.add_class("active")
        loading_bar.styles.opacity = 0.5
        loading_bar.styles.animate("opacity", 1.0, duration=0.5, easing="in_out_sine")

        try:
            response = await self.ai_service.get_response(
                self.current_model["display_name"], self.current_model["provider_api"],
                text, system_prompt=self.current_persona["system_prompt"]
            )
            await chat_log.mount(ChatMessage(response, "ai", middleware=self.middleware))
            chat_log.scroll_end()
            self.chat_history.append({"sender": "ai", "text": response, "model": self.current_model["display_name"], "timestamp": str(datetime.now())})
            self._save_history()
            if not self.is_authenticated:
                self.guest_queries += 1
        except Exception:
            self.notify(fix_persian(self.config["strings"]["error_connection"]), severity="error")
        finally:
            loading_bar.remove_class("active")

    async def action_toggle_admin(self):
        def check_login(success):
            if success:
                screen_cfg = ScreenRegistry.get_screen("admin_panel")
                self.push_screen(screen_cfg["class"](self.config, self.models))

        login_cfg = ScreenRegistry.get_screen("admin_login")
        await self.push_screen(login_cfg["class"](self.config["admin_secret"]), check_login)

    async def on_unmount(self):
        await self.ai_service.close()

if __name__ == "__main__":
    app = BugattiApp()
    app.run()
