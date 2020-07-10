class EventSourcer():
    # Do not change the signature of any functions

    def __init__(self):
        self.value = 0
        self._event_stack = [0]
        self._event_index = 0

    def add(self, num: int):
        self._reset_future()
        self.value += num
        self._event_stack.append(self.value)
        self._event_index += 1

    def subtract(self, num: int):
        self._reset_future()
        self.value -= num
        self._event_stack.append(self.value)
        self._event_index += 1

    def undo(self):
        if self._event_index - 1 < 0:  # Test that we have anything to undo
            return
        self._event_index -= 1
        self.value = self._event_stack[self._event_index]

    def redo(self):
        if self._event_index + 1 >= len(self._event_stack):  # Test that we have anything to redo
            return
        self._event_index += 1
        self.value = self._event_stack[self._event_index]

    def bulk_undo(self, steps: int):
        new_index = self._event_index - steps
        if new_index < 0:  # Are we trying to go back further in time than possible?
            self._event_index = 0  # If so, just go as far as we can
        else:
            self._event_index = new_index
        self.value = self._event_stack[self._event_index]

    def bulk_redo(self, steps: int):
        new_index = self._event_index + steps
        if new_index >= len(self._event_stack):  # Are we trying to redo more than possible?
            self._event_index = len(self._event_stack) - 1  # If so, redo as much as we can
        else:
            self._event_index = new_index
        self.value = self._event_stack[self._event_index]

    def _reset_future(self):
        self._event_stack = self._event_stack[0:self._event_index + 1]
