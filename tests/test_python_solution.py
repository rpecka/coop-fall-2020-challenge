import json
import pytest

from solution_python import EventSourcer

def test_add():
    sourcer = EventSourcer()

    sourcer.add(2)
    sourcer.add(5)

    assert sourcer.value == 7

def test_subtract():
    sourcer = EventSourcer()

    sourcer.subtract(2)
    sourcer.subtract(5)

    assert sourcer.value == -7

def test_undo():
    sourcer = EventSourcer()

    sourcer.add(2)
    sourcer.add(2)
    sourcer.add(2)
    sourcer.add(2)
    sourcer.undo()

    assert sourcer.value == 6

def test_redo():
    sourcer = EventSourcer()

    sourcer.add(5)
    sourcer.add(5)
    sourcer.add(5)
    sourcer.undo()
    sourcer.undo()
    sourcer.add(1)
    sourcer.redo()

    assert sourcer.value == 11

def test_bulk_undo():
    sourcer = EventSourcer()

    sourcer.add(1)
    sourcer.add(2)
    sourcer.add(3)
    sourcer.add(4)
    sourcer.add(5)
    sourcer.bulk_undo(3)

    assert sourcer.value == 3

def test_bulk_redo():
    sourcer = EventSourcer()

    sourcer.add(1)
    sourcer.add(1)
    sourcer.add(1)
    sourcer.add(1)
    sourcer.add(1)
    sourcer.undo()
    sourcer.undo()
    sourcer.undo()
    sourcer.undo()

    sourcer.bulk_redo(4)

    assert sourcer.value == 5

def test_undo_no_actions():
    sourcer = EventSourcer()

    sourcer.undo()

    assert sourcer.value == 0

def test_redo_with_no_redo_step():
    sourcer = EventSourcer()

    sourcer.redo()

    assert sourcer.value == 0

def test_bulk_undo_overstep():
    sourcer = EventSourcer()

    sourcer.add(5)
    sourcer.add(5)
    sourcer.add(5)
    sourcer.add(5)
    sourcer.subtract(5)
    sourcer.bulk_undo(5)

    assert sourcer.value == 0

def test_bulk_redo_overstep():
    sourcer = EventSourcer()

    sourcer.add(5)
    sourcer.add(5)
    sourcer.add(5)
    sourcer.add(5)
    sourcer.add(5)
    sourcer.undo()
    sourcer.undo()
    sourcer.undo()
    assert sourcer.value == 10
    sourcer.bulk_redo(5)

    assert sourcer.value == 25

def test_bulk_undo_no_actions():
    sourcer = EventSourcer()

    sourcer.bulk_undo(1)
    assert sourcer.value == 0

    sourcer.bulk_undo(500)
    assert sourcer.value == 0

def test_bulk_redo_with_no_redo_step():
    sourcer = EventSourcer()

    sourcer.bulk_redo(1)
    assert sourcer.value == 0

    sourcer.bulk_redo(500)
    assert sourcer.value == 0

def test_invalid_undo_steps():
    sourcer = EventSourcer()

    sourcer.add(5)
    sourcer.bulk_undo(-1)
    assert sourcer.value == 5

def test_invalid_redo_steps():
    sourcer = EventSourcer()

    sourcer.add(5)
    sourcer.add(5)
    sourcer.undo()
    sourcer.bulk_redo(-1)
    assert sourcer.value == 5

def test_commit_undo_retain_value():
    sourcer = EventSourcer()

    sourcer.add(5)
    sourcer.commit()
    assert sourcer.value == 5

    sourcer.undo()
    assert sourcer.value == 5

def test_commit_redo_retain_value():
    sourcer = EventSourcer()

    sourcer.add(5)
    sourcer.add(5)
    sourcer.undo()
    sourcer.commit()
    assert sourcer.value == 5

    sourcer.redo()
    assert sourcer.value == 5
