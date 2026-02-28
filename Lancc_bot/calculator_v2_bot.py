# -*- coding: utf-8 -*-
# Telegram Calculator Bot v2

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8626674822:AAFARYLNoMpei2xe3yuHmYGOS5FmM4mxOG4"

RATE = 7.6
deposits = []
withdraws = []


# 开始
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "新·计算器 v2 🤖\n\n"
        "/add 数字 → 添加入款\n"
        "/withdraw 数字 → 添加下发\n"
        "/rate 数字 → 设置汇率\n"
        "/result → 查看统计\n"
        "/clear → 清空数据"
    )


# 添加入款
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(context.args[0])
        deposits.append(amount)
        await update.message.reply_text(f"已添加入款: {amount}")
    except:
        await update.message.reply_text("用法: /add 1000")


# 添加下发
async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(context.args[0])
        withdraws.append(amount)
        await update.message.reply_text(f"已添加下发: {amount}")
    except:
        await update.message.reply_text("用法: /withdraw 500")


# 设置汇率
async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global RATE
    try:
        RATE = float(context.args[0])
        await update.message.reply_text(f"汇率已设置为: {RATE}")
    except:
        await update.message.reply_text("用法: /rate 7.6")


# 查看结果
async def result(update: Update, context: ContextTypes.DEFAULT_TYPE):

    total_deposit = sum(deposits)
    total_withdraw = sum(withdraws)

    deposit_u = total_deposit / RATE if RATE else 0
    withdraw_u = total_withdraw / RATE if RATE else 0

    remain = total_deposit - total_withdraw
    remain_u = remain / RATE if RATE else 0

    text = "新·计算器 v2\n\n"

    text += f"入款（{len(deposits)}笔）\n"
    for d in deposits:
        text += f"{d} / {RATE} = {round(d/RATE,2)}u\n"

    text += f"\n下发（{len(withdraws)}笔）\n"
    for w in withdraws:
        text += f"{w} / {RATE} = {round(w/RATE,2)}u\n"

    text += f"\n汇率: {RATE}\n"

    text += f"\n总入款: {total_deposit}\n"
    text += f"应下发: {total_deposit} | {round(deposit_u,2)}u\n"
    text += f"已下发: {total_withdraw} | {round(withdraw_u,2)}u\n"
    text += f"未下发: {remain} | {round(remain_u,2)}u\n"

    await update.message.reply_text(text)


# 清空
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deposits.clear()
    withdraws.clear()
    await update.message.reply_text("数据已清空")


# 主程序
def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("withdraw", withdraw))
    app.add_handler(CommandHandler("rate", rate))
    app.add_handler(CommandHandler("result", result))
    app.add_handler(CommandHandler("clear", clear))

    print("机器人已启动...")
    app.run_polling()


if __name__ == "__main__":
    main()
