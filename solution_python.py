class EventSourcer():
    # Do not change the signature of any functions

    def __init__(self):
        self.value = 0
        self._event_stack = []
        self._event_index = -1

    def add(self, num: int):
        self.value += num
        self._event_index += 1
        if self._event_index < len(self._event_stack):
            self._event_stack[self._event_index] = num
        else:
            self._event_stack.append(num)

    def subtract(self, num: int):
        self.value -= num
        self._event_index += 1
        if self._event_index < len(self._event_stack):
            self._event_stack[self._event_index] = num * -1
        else:
            self._event_stack.append(num * -1)

    def undo(self):
        if self._event_index < 0:
            return
        self.value -= self._event_stack[self._event_index]
        self._event_index -= 1

    def redo(self):
        if self._event_index >= len(self._event_stack) - 1:
            return
        self._event_index += 1
        self.value += self._event_stack[self._event_index]

    def bulk_undo(self, steps: int):
        if self._event_index - steps < -1:
            remaining_steps = self._event_index + 1
        else:
            remaining_steps = steps
        while remaining_steps > 0:
            self.value -= self._event_stack[self._event_index]
            self._event_index -= 1
            remaining_steps -= 1

    def bulk_redo(self, steps: int):
        if self._event_index + steps >= len(self._event_stack):
            remaining_steps = len(self._event_stack) - self._event_index - 1
        else:
            remaining_steps = steps
        while remaining_steps > 0:
            self._event_index += 1
            self.value += self._event_stack[self._event_index]
            remaining_steps -= 1
