from aiogram.fsm.state import State, StatesGroup


class SearchFlow(StatesGroup):
    choosing_origin = State()
    choosing_destination = State()
    choosing_date = State()
    entering_date_manual = State()
    entering_date_range = State()
    previewing = State()
