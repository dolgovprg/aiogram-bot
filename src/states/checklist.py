from aiogram.dispatcher.filters.state import State, StatesGroup
# States
class CheckList(StatesGroup):
    location = State()  
    answers = State()  
    image = State()  