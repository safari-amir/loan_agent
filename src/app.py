import streamlit as st
from agent.agent import agent
import time

# ----------------------------
# تنظیمات صفحه
# ----------------------------
st.set_page_config(
    page_title="💰 چت‌بات مدیریت وام بانکی",
    page_icon="🏦",
    layout="centered"
)

# ----------------------------
# استایل راست‌چین و فونت فارسی
# ----------------------------
rtl_css = """
<style>
body {
    direction: rtl;
    text-align: right;
}
.stChatMessage {
    text-align: right;
}
.stTextInput, .stTextArea {
    direction: rtl;
    text-align: right;
}
.st-expander summary {
    direction: rtl;
}
p, div, span, h1, h2, h3, h4, h5, h6 {
    direction: rtl;
    text-align: right;
}
</style>
"""
st.markdown(rtl_css, unsafe_allow_html=True)

# ----------------------------
# عنوان صفحه
# ----------------------------
st.title("💬 چت‌بات هوشمند سامانه درخواست وام")
st.markdown("سؤالات خود را درباره‌ی وام‌ها، وضعیت درخواست، یا مدارک لازم بنویسید 👇")

st.markdown("---")

# ----------------------------
# راه‌اندازی حافظه مکالمه
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "سلام 👋 من دستیار هوشمند بانک هستم. می‌تونم در مورد درخواست وام یا پیگیری وضعیتت کمکت کنم."}
    ]

# ----------------------------
# نمایش تاریخچه‌ی چت
# ----------------------------
for msg in st.session_state.messages:
    avatar = "🧑‍💼" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ----------------------------
# بخش ورود سؤال توسط کاربر
# ----------------------------
if query := st.chat_input("سؤال خود را بنویسید..."):
    # ثبت و نمایش پیام کاربر
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user", avatar="🧑‍💼"):
        st.markdown(query)

    # پاسخ‌دهی مرحله‌ای از طریق Agent
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        msg = ""

        try:
            # استریم پاسخ از عامل (Agent)
            for step in agent.stream(
                {"messages": [{"role": "user", "content": query}]},
                {"configurable": {"thread_id": "1"}},
                stream_mode="values",
            ):
                step["messages"][-1].pretty_print()
            msg = step["messages"][-1].content

            # نمایش پاسخ
            placeholder.markdown(msg)
            time.sleep(0.03)

            # ذخیره پاسخ در تاریخچه
            st.session_state.messages.append({"role": "assistant", "content": msg.strip()})

        except Exception as e:
            st.error(f"❌ خطا در پردازش درخواست: {e}")
            st.session_state.messages.append({"role": "assistant", "content": f"خطا: {e}"})
