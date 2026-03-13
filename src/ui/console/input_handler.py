from __future__ import annotations


class InputHandler:
    def ask(self, prompt: str = "Your choice") -> str:
        return input(f"\n{prompt}: ").strip()

    def pause(self) -> None:
        input("\nPress Enter to continue...")