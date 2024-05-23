from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

default_watermark = InlineKeyboardButton(
    text='Default',
    callback_data='default_watermark'
)
custom_watermark = InlineKeyboardButton(
    text='Custom',
    callback_data='custom_watermark'
)
choose_watermark = InlineKeyboardMarkup(
    inline_keyboard=[[default_watermark, custom_watermark]]
)


transparency_10 = InlineKeyboardButton(
    text='10%',
    callback_data='transparency_10'
)
transparency_20 = InlineKeyboardButton(
    text='20%',
    callback_data='transparency_20'
)
transparency_30 = InlineKeyboardButton(
    text='30%',
    callback_data='transparency_30'
)
transparency_40 = InlineKeyboardButton(
    text='40%',
    callback_data='transparency_40'
)
transparency_50 = InlineKeyboardButton(
    text='50%',
    callback_data='transparency_50'
)
transparency_60 = InlineKeyboardButton(
    text='60%',
    callback_data='transparency_60'
)
transparency_70 = InlineKeyboardButton(
    text='70%',
    callback_data='transparency_70'
)
transparency_80 = InlineKeyboardButton(
    text='80%',
    callback_data='transparency_80'
)
transparency_90 = InlineKeyboardButton(
    text='90%',
    callback_data='transparency_90'
)
transparency_0 = InlineKeyboardButton(
    text='0%',
    callback_data='transparency_0'
)
choose_transparency = InlineKeyboardMarkup(
    inline_keyboard=[[transparency_10, transparency_20, transparency_30],
                     [transparency_40, transparency_50, transparency_60],
                     [transparency_70, transparency_80, transparency_90], [transparency_0]]
)


position_up_left = InlineKeyboardButton(
    text='Up Left',
    callback_data='position_up_left'
)
position_up_right = InlineKeyboardButton(
    text='Up Right',
    callback_data='position_up_right'
)
position_center = InlineKeyboardButton(
    text='Center',
    callback_data='position_center'
)
position_whole_image = InlineKeyboardButton(
    text='Whole Image',
    callback_data='position_whole_image'
)
position_down_left = InlineKeyboardButton(
    text='Down Left',
    callback_data='position_down_left'
)
position_down_right = InlineKeyboardButton(
    text='Down Right',
    callback_data='position_down_right'
)
choose_position = InlineKeyboardMarkup(
    inline_keyboard=[[position_up_left, position_up_right], [position_center, position_whole_image], [position_down_left, position_down_right]]
)


size_small = InlineKeyboardButton(
    text='Small',
    callback_data='size_small'
)
size_medium = InlineKeyboardButton(
    text='Medium',
    callback_data='size_medium'
)
size_large = InlineKeyboardButton(
    text='Large',
    callback_data='size_large'
)
size_xlarge = InlineKeyboardButton(
    text='XL (Unstable)',
    callback_data='size_xlarge'
)
choose_size = InlineKeyboardMarkup(
    inline_keyboard=[[size_small, size_medium, size_large], [size_xlarge]]
)


color_white = InlineKeyboardButton(
    text='White',
    callback_data='color_white'
)
color_black = InlineKeyboardButton(
    text='Black',
    callback_data='color_black'
)
choose_color = InlineKeyboardMarkup(
    inline_keyboard=[[color_white, color_black]]
)