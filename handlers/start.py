from aiogram import filters, types, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from buttons.reply_buttons import contact_button
from aiogram.types import ReplyKeyboardRemove


router = Router()


class Registration(StatesGroup):
    full_name = State()
    phone_number = State()


@router.message(filters.Command("start"))
async def start_function(message: types.Message,
                         state: FSMContext):
    user_check = db.check_user(message.from_user.id)
    if user_check is None:

        await db.create_table_users()
        await state.set_state(Registration.full_name)
        await message.answer(f"Привет дорогой человек, "
                             f"отправьте фамилю и имя")
    else:
        await message.answer("С возвращением")


@router.message(Registration.full_name)
async def full_name_function(message: types.Message,
                             state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    await state.set_state(Registration.phone_number)
    await message.answer("Отлично, теперь отправь "
                         "мне свой номер",
                         reply_markup=contact_button)


@router.message(Registration.phone_number)
async def phone_number_function(message: types.Message,
                                state: FSMContext):
    phone_number = message.contact.phone_number
    data = await state.get_data()
    db.add_user(id=message.from_user.id, full_name=data['full_name'],
                phone_number=data['phone_number'])


    await state.update_data(phone_number=phone_number)
    await message.answer("Отлично, мы сохранили ваши данные",
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()
