class EventSourcer():
    # Do not change the signature of any functions

    def __init__(self):
        self.value = 0

        # Store a list of changes that have been made. Apply a change by adding the values in this array,
        # revert a change by subtracting it
        self._event_list = []

        # Keep track of where we are in the list of events. Start at -1 so that we don't have to store a
        # useless value at index 0 when we have made no changes. A value of -1 indicates that we are at the original
        # value
        self._event_index = -1

    def add(self, num: int):
        self._push_event(num)

    def subtract(self, num: int):
        self._push_event(num * -1)  # Push the opposite of num to indicate subtraction

    # Push an event onto the stack. To push a subtraction, push a negative number
    def _push_event(self, num):
        self.value += num  # Update the current value
        self._event_index += 1
        if self._event_index < len(self._event_list):  # If there is a future entry in front of us, update it
            self._event_list[self._event_index] = num
        else:  # Otherwise we need to increase the size of our stack
            self._event_list.append(num)

    def undo(self):
        if self._event_index < 0:  # Check that we have something to undo
            return
        # Revert the current event and then move to the previous one
        self.value -= self._event_list[self._event_index]
        self._event_index -= 1

    def redo(self):
        if self._event_index >= len(self._event_list) - 1:  # Check that we have something to redo
            return
        # Move to the next event and apply it
        self._event_index += 1
        self.value += self._event_list[self._event_index]

    def bulk_undo(self, steps: int):
        if steps < 0:
            return

        # Determine the number of remaining steps in advance so that we don't have to repeat bounds checking
        if self._event_index - steps < -1:  # Check if we are trying to undo more than we can
            remaining_steps = self._event_index + 1
        else:
            remaining_steps = steps
        # Iterate over the list of events and revert each of them
        while remaining_steps > 0:
            self.value -= self._event_list[self._event_index]
            self._event_index -= 1
            remaining_steps -= 1

    def bulk_redo(self, steps: int):
        if steps < 0:
            return

        # Determine the number of remaining steps in advance so that we don't have to repeat bounds checking
        if self._event_index + steps >= len(self._event_list):  # Check if we are trying to redo more than we can
            remaining_steps = len(self._event_list) - self._event_index - 1
        else:
            remaining_steps = steps
        # Iterate over the list of events and apply them
        while remaining_steps > 0:
            self._event_index += 1
            self.value += self._event_list[self._event_index]
            remaining_steps -= 1
