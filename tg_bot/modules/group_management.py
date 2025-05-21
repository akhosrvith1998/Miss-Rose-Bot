from . import group_management
def is_group_active(chat_id):
    import json, datetime
    with open('groups.json', 'r') as f:
        groups = json.load(f)
    expire_str = groups.get(str(chat_id))
    if not expire_str:
        return False
    expire_date = datetime.datetime.strptime(expire_str, "%Y-%m-%d")
    return datetime.datetime.now() < expire_date
@client.on_message(filters.command(["ویژه"]) & filters.group)
def add_vip(_, message):
    if not message.reply_to_message:
        return message.reply("روی پیام کاربر ریپلای کن یا یوزرنیم بده.")
    user = message.reply_to_message.from_user.id
    group_id = str(message.chat.id)

    with open("vips.json", "r+") as f:
        data = json.load(f)
        data.setdefault(group_id, [])
        if user not in data[group_id]:
            data[group_id].append(user)
        f.seek(0)
        json.dump(data, f)
        f.truncate()
    message.reply("✅ کاربر ویژه شد.")

@client.on_message(filters.command(["حذف_ویژه"]) & filters.group)
def remove_vip(_, message):
    if not message.reply_to_message:
        return message.reply("روی پیام کاربر ریپلای کن.")
    user = message.reply_to_message.from_user.id
    group_id = str(message.chat.id)

    with open("vips.json", "r+") as f:
        data = json.load(f)
        if group_id in data and user in data[group_id]:
            data[group_id].remove(user)
        f.seek(0)
        json.dump(data, f)
        f.truncate()
    message.reply("❌ کاربر از لیست ویژه حذف شد.")
@client.on_message(filters.command(["شارژ"]) & filters.user(OWNER_ID))
def charge_group(_, message):
    try:
        args = message.text.split()
        days = int(args[1])
        group_id = str(message.chat.id)
        expire = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        with open('groups.json', 'r+') as f:
            data = json.load(f)
            data[group_id] = expire
            f.seek(0)
            json.dump(data, f)
            f.truncate()
        message.reply(f"✅ گروه به مدت {days} روز شارژ شد.")
    except:
        message.reply("فرمت درست: شارژ 30")

@client.on_message(filters.command(["حذف"]) & filters.user(OWNER_ID))
def delete_group(_, message):
    with open('groups.json', 'r+') as f:
        data = json.load(f)
        data.pop(str(message.chat.id), None)
        f.seek(0)
        json.dump(data, f)
        f.truncate()
    message.reply("❌ گروه از لیست حذف شد.")

@client.on_message(filters.command(["لیست"]) & filters.user(OWNER_ID))
def list_groups(_, message):
    with open('groups.json') as f:
        data = json.load(f)
    text = "\n".join([f"{gid}: {exp}" for gid, exp in data.items()])
    message.reply(f"📋 لیست گروه‌های شارژ شده:\n\n{text}")