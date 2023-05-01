#!/usr/bin/python3
from models import storage
from models.state import State


pl = State()
print(pl.__class__.__name__)
print(storage.all(State))
