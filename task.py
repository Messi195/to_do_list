from typing import Optional
import customtkinter as ctk


class Task:
    """
    A class that describes a task in a to_do list.
    """
    __slots__ = ('_description', '_completed', 'widget_frame')

    def __init__(self, description: str) -> None:
        self._description = description.strip()
        self._completed = False
        self.widget_frame: Optional[ctk.CTkFrame] = None
        
    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str) -> None:
        if value:
            self._description = value.strip()

    @property
    def completed(self) -> bool:
        return self._completed
    
    @completed.setter
    def completed(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError('completed must be bool!')
        self._completed = value

