from __future__ import annotations

from typing import Iterable

from ulauncher.api.result import Result
from ulauncher.api.shared.query import Query


class BaseMode:
    def is_enabled(self, _query: Query) -> bool:
        """
        Return True if mode should be enabled for a query
        """
        return False

    def on_query_change(self, _query: Query) -> None:
        """
        Triggered when user changes a search query
        """

    def on_query_backspace(self, _query: Query) -> str | None:
        """
        Return string to override default backspace and set the query to that string
        """
        return None

    # TODO(friday): Get rid of bool type (only used in DeferredResultRenderer.handle_event to keep window open)
    def handle_query(self, _query: Query) -> bool | Iterable[Result]:
        return []

    def get_triggers(self) -> Iterable[Result]:
        return []

    def get_fallback_results(self) -> Iterable[Result]:
        """
        If nothing matches the user input
        """
        return []
