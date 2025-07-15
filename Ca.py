# Replace the existing help button section with this updated version
elif query.data == "help":
    user_id = query.from_user.id
    if await is_banned(user_id):
        await query.message.edit_text("❌ You are banned by the bot owner.")
        return
    buttons = [[
        InlineKeyboardButton('📝 Caption', callback_data='caption_setting'),
        InlineKeyboardButton('🧧 Font', callback_data='set_font')
    ],[
        InlineKeyboardButton('👤 Usernames', callback_data='rem_username'),
        InlineKeyboardButton('🔗 Links', callback_data='rem_links')
    ],[
        InlineKeyboardButton('🚫 Blacklist', callback_data='word_blacklist'),
        InlineKeyboardButton('😀 Emoji', callback_data='rem_emoji')
    ],[
        InlineKeyboardButton('🔄 Replace Words', callback_data='words_replace'),
        InlineKeyboardButton('🗑 Remove Words', callback_data='rem_words')
    ],[
        InlineKeyboardButton('🔠 Prefix', callback_data='prefix_code'),
        InlineKeyboardButton('🔚 Suffix', callback_data='suffix_code')
    ],[
        InlineKeyboardButton('🔣 Symbols', callback_data='rem_symbols'),
        InlineKeyboardButton('🧾 Space/Line', callback_data='space_line')
    ],[
        InlineKeyboardButton('🌐 Language', callback_data='lang_settings'),  # New button
        InlineKeyboardButton('🎬 Quality', callback_data='quality_settings')  # New button
    ],[
        ,  # New button
        InlineKeyboardButton('🔘 Buttons', callback_data='button_settings')  # New button
    ],[
        InlineKeyboardButton('📇 Details', callback_data='chk_details'),
        InlineKeyboardButton('💣 Reset', callback_data='reset_cmds')
    ],[
        InlineKeyboardButton('🏠 Back to Home', callback_data='start')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=script.HELP_TXT,
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML
    )

# Add these new callback handlers after the existing ones
elif query.data == "lang_settings":
    buttons = [[
        InlineKeyboardButton('↩ Back', callback_data='help'),
        InlineKeyboardButton('👨🏻‍💻 Support', url=SUPPORT)
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=script.LANG_SETTINGS_TXT,
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML
    )

elif query.data == "quality_settings":
    buttons = [[
        InlineKeyboardButton('↩ Back', callback_data='help'),
        InlineKeyboardButton('👨🏻‍💻 Support', url=SUPPORT)
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=script.QUALITY_SETTINGS_TXT,
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML
    )

elif query.data == "protect_words":
    buttons = [[
        InlineKeyboardButton('↩ Back', callback_data='help'),
        InlineKeyboardButton('👨🏻‍💻 Support', url=SUPPORT)
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=script.PROTECT_WORDS_TXT,
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML
    )

elif query.data == "button_settings":
    buttons = [[
        InlineKeyboardButton('↩ Back', callback_data='help'),
        InlineKeyboardButton('👨🏻‍💻 Support', url=SUPPORT)
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=script.BUTTON_SETTINGS_TXT,
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML
)

# ... existing code ...

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    # ... existing callbacks ...
    
    elif query.data == "help":
        user_id = query.from_user.id
        if await is_banned(user_id):
            await query.message.edit_text("❌ You are banned by the bot owner.")
            return
        buttons = [[
            InlineKeyboardButton('📝 Caption', callback_data='caption_setting'),
            InlineKeyboardButton('🈲 Font', callback_data='set_font')
        ],[
            InlineKeyboardButton('👤 Usernames', callback_data='rem_username'),
            InlineKeyboardButton('🔗 Links', callback_data='rem_links')
        ],[
            InlineKeyboardButton('🚫 Blacklist', callback_data='word_blacklist'),
            InlineKeyboardButton('😀 Emoji', callback_data='rem_emoji')
        ],[
            InlineKeyboardButton('🔄 Replace Words', callback_data='words_replace'),
            InlineKeyboardButton('🗑 Remove Words', callback_data='rem_words')
        ],[
            InlineKeyboardButton('🔠 Prefix', callback_data='prefix_code'),
            InlineKeyboardButton('🔚 Suffix', callback_data='suffix_code')
        ],[
            InlineKeyboardButton('🔣 Symbols', callback_data='rem_symbols'),
            InlineKeyboardButton('🧾 Space/Line', callback_data='space_line')
        ],[
            InlineKeyboardButton('🖼 Buttons & Ext', callback_data='buttons_ext')
        ],[
            InlineKeyboardButton('📇 Details', callback_data='chk_details'),
            InlineKeyboardButton('💣 Reset', callback_data='reset_cmds')
        ],[
            InlineKeyboardButton('🏠 Back to Home', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.HELP_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    # New sections
    elif query.data == "lang_quality":
        buttons = [[
            InlineKeyboardButton('↩ Back', callback_data='help'),
            InlineKeyboardButton('👨🏻‍💻 Support', url=SUPPORT)
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.LANG_QUALITY_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query.data == "buttons_ext":
        buttons = [[
            InlineKeyboardButton('↩ Back', callback_data='help'),
            InlineKeyboardButton('👨🏻‍💻 Support', url=SUPPORT)
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTONS_EXT_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    # Updated symbols section
    elif query.data == "rem_symbols":
        buttons = [[
            InlineKeyboardButton('↩ Back', callback_data='help'),
            InlineKeyboardButton('👨🏻‍💻 Support', url=SUPPORT)
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SYMBOL_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

# ... rest of the code ...
