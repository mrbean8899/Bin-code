# ... existing code ...

# Define new helper function to generate protected ranges
def get_protected_ranges(caption, protected_words):
    protected_ranges = []
    if not protected_words:
        return protected_ranges
        
    for word in protected_words:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        for match in pattern.finditer(caption):
            start = match.start()
            end = match.end()
            protected_ranges.append((start, end))
            
    # Sort ranges by start position and merge overlapping ranges
    protected_ranges.sort(key=lambda x: x[0])
    merged = []
    for start, end in protected_ranges:
        if not merged:
            merged.append((start, end))
        else:
            last_start, last_end = merged[-1]
            if start <= last_end:
                merged[-1] = (last_start, max(last_end, end))
            else:
                merged.append((start, end))
                
    return merged

# Update remove_symbols function to support protected words
def remove_symbols(caption, symbols, protected_words=None):
    if not caption or not symbols:
        return caption
        
    # If no protected words, do simple removal
    if not protected_words:
        return re.sub(f"[{re.escape(symbols)}]", '', caption)
    
    # Get protected ranges
    protected_ranges = get_protected_ranges(caption, protected_words)
    
    new_chars = []
    i = 0
    while i < len(caption):
        protected = False
        for start, end in protected_ranges:
            if start <= i < end:
                # Add entire protected segment
                new_chars.append(caption[i:end])
                i = end
                protected = True
                break
                
        if protected:
            continue
            
        # If not protected, check if symbol should be removed
        if caption[i] not in symbols:
            new_chars.append(caption[i])
            
        i += 1
        
    return ''.join(new_chars)

# Update replace_symbols_with_space to support protected words
def replace_symbols_with_space(caption, symbols, protected_words=None):
    if not caption or not symbols:
        return caption
        
    # If no protected words, do simple replacement
    if not protected_words:
        return re.sub(f"[{re.escape(symbols)}]", ' ', caption)
    
    # Get protected ranges
    protected_ranges = get_protected_ranges(caption, protected_words)
    
    new_chars = []
    i = 0
    while i < len(caption):
        protected = False
        for start, end in protected_ranges:
            if start <= i < end:
                # Add entire protected segment
                new_chars.append(caption[i:end])
                i = end
                protected = True
                break
                
        if protected:
            continue
            
        # If not protected, replace symbol with space
        if caption[i] in symbols:
            new_chars.append(' ')
        else:
            new_chars.append(caption[i])
            
        i += 1
        
    return ''.join(new_chars)

# ... existing code ...

# Add new protected words commands
@Client.on_message(filters.command("protect_sym_words") & filters.channel)
async def set_protected_words(bot, message):
    chnl_id = message.chat.id
    if len(message.command) < 2:
        chkData = await chnl_ids.find_one({"chnl_id": chnl_id})
        if chkData and "protected_words" in chkData:
            return await message.reply(
                "🛡 Current protected words:\n" +
                "\n".join([f"• {w}" for w in chkData["protected_words"]])
            )
        return await message.reply("Usage: /protect_sym_words word1|word2|phrase...")
    
    input_text = message.text.split(" ", 1)[1].strip()
    words = [w.strip() for w in input_text.split("|") if w.strip()]
    
    if not words:
        return await message.reply("⚠️ Please provide at least one word/phrase to protect")
    
    chkData = await chnl_ids.find_one({"chnl_id": chnl_id}) or {}
    existing = chkData.get("protected_words", [])
    seen = set(w.lower() for w in existing)
    new_words = existing.copy()
    added = []
    
    for word in words:
        if word.lower() not in seen:
            new_words.append(word)
            seen.add(word.lower())
            added.append(word)
    
    await chnl_ids.update_one(
        {"chnl_id": chnl_id},
        {"$set": {"protected_words": new_words}},
        upsert=True
    )
    
    response = f"✅ Added {len(added)} protected words:\n"
    response += "\n".join([f"• {w}" for w in added])
    response += f"\n\nTotal protected words: {len(new_words)}"
    await message.reply(response)

@Client.on_message(filters.command("protect_sym_list") & filters.channel)
async def show_protected_words(bot, message):
    chnl_id = message.chat.id
    chkData = await chnl_ids.find_one({"chnl_id": chnl_id})
    if chkData and "protected_words" in chkData and chkData["protected_words"]:
        words = chkData["protected_words"]
        response = "🛡 Current protected words:\n\n"
        response += "\n".join([f"• {word}" for word in words])
        response += f"\n\nTotal: {len(words)} words"
        await message.reply(response)
    else:
        await message.reply("ℹ️ No words are currently protected")

@Client.on_message(filters.command("rem_protect_rule") & filters.channel)
async def remove_protected_words(bot, message):
    chnl_id = message.chat.id
    try:
        if len(message.command) < 2:
            chkData = await chnl_ids.find_one({"chnl_id": chnl_id})
            if not chkData or "protected_words" not in chkData:
                return await message.reply("ℹ️ No words are currently protected.")
            words = chkData["protected_words"]
            response = (
                "🛡 Current protected words:\n\n" +
                "\n".join([f"• {w}" for w in words]) +
                f"\n\nTotal: {len(words)} words\n\n"
                "Usage: /rem_protect_rule word1|word2|phrase"
            )
            return await message.reply(response)
        
        input_text = message.text.split(" ", 1)[1].strip()
        words_to_remove = [w.strip() for w in input_text.split("|") if w.strip()]
        
        if not words_to_remove:
            return await message.reply("⚠️ Please provide at least one word/phrase to unprotect")
        
        chkData = await chnl_ids.find_one({"chnl_id": chnl_id})
        if not chkData or "protected_words" not in chkData or not chkData["protected_words"]:
            return await message.reply("ℹ️ No words are currently protected.")
        
        current_words = chkData["protected_words"]
        remove_lower = set(word.lower() for word in words_to_remove)
        removed = [word for word in current_words if word.lower() in remove_lower]
        
        if not removed:
            return await message.reply("❌ None of the specified words were found in the protected list")
        
        new_words = [word for word in current_words if word.lower() not in remove_lower]
        
        await chnl_ids.update_one(
            {"chnl_id": chnl_id},
            {"$set": {"protected_words": new_words}}
        )
        
        response = f"✅ Removed {len(removed)} words from protection:\n"
        response += "\n".join([f"• {word}" for word in removed])
        response += f"\n\nCurrent protected words ({len(new_words)}):\n"
        response += "\n".join([f"• {word}" for word in new_words])
        await message.reply(response)
    except Exception as e:
        await message.reply(f"⚠️ Error: {str(e)}")
        traceback.print_exc()

@Client.on_message(filters.command("clear_protect_list") & filters.channel)
async def clear_protected_words(bot, message):
    chnl_id = message.chat.id
    await chnl_ids.update_one(
        {"chnl_id": chnl_id},
        {"$unset": {"protected_words": ""}}
    )
    await message.reply("✅ All protected words cleared")

# Update reCap function to pass protected words to symbol functions
@Client.on_message(filters.channel)
async def reCap(bot, message):
    # ... existing code ...
    
    # Apply transformations
    protected_words = cap_dets.get("protected_words", [])
    
    if "words_to_remove" in cap_dets:
        replaced_caption = remove_words_from_caption(
            replaced_caption, 
            cap_dets["words_to_remove"]
        )
        
    if "word_replacements" in cap_dets:
        replaced_caption = replace_words(
            replaced_caption, 
            cap_dets["word_replacements"]
        )
        
    if "symbols_to_remove" in cap_dets:
        replaced_caption = remove_symbols(
            replaced_caption, 
            cap_dets["symbols_to_remove"],
            protected_words=protected_words
        )
        
    if cap_dets.get("remove_all_usernames"):
        replaced_caption = remove_usernames(replaced_caption)
        
    if cap_dets.get("remove_links"):
        replaced_caption = remove_links(replaced_caption)
        
    if "symbols_to_replace" in cap_dets and cap_dets["symbols_to_replace"]:
        replaced_caption = replace_symbols_with_space(
            replaced_caption, 
            cap_dets["symbols_to_replace"],
            protected_words=protected_words
        )
        
    # ... rest of the code remains the same ...

# Update show_all_settings to include protected words
@Client.on_message(filters.command("show_details") & filters.channel)
async def show_all_settings(bot, message):
    # ... existing code ...
    
    if "protected_words" in cap_dets and cap_dets["protected_words"]:
        words = cap_dets["protected_words"]
        response += f"🛡 <b>Protected words ({len(words)}):</b>\n"
        response += "\n".join([f"• {w}" for w in words]) + "\n\n"
    else:
        response += "🛡 <b>Protected words:</b> None\n\n"
    
    # ... rest of the code remains the same ...
