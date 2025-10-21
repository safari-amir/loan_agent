import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from database.models import Base, Customer, LoanRequest
import os

# -------------------------------
# تنظیمات پایگاه داده
# -------------------------------
DATABASE_URL = "sqlite:///loan_management.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

st.set_page_config(page_title="درخواست وام بانکی", page_icon="🏦", layout="centered")

st.title("🏦 فرم درخواست وام بانکی")

# -------------------------------
# دریافت کد ملی
# -------------------------------
national_id = st.text_input("کد ملی خود را وارد کنید:")

if national_id:
    customer = session.query(Customer).filter_by(national_id=national_id).first()

    if customer:
        st.success("✅ اطلاعات شما در سیستم یافت شد.")
        st.write("**نام:**", customer.first_name, customer.last_name)
        st.write("**شماره حساب:**", customer.account_number)
        st.write("**موجودی حساب:**", f"{customer.account_balance:,.0f} ریال")
        st.write("**درآمد ماهیانه:**", f"{customer.monthly_income:,.0f} ریال")
        st.write("---")

        # فرم درخواست وام
        st.subheader("📋 ثبت درخواست وام جدید")

        loan_type = st.selectbox(
            "نوع وام:",
            ["خرید مسکن", "خودرو", "ازدواج", "کالا و خدمات", "آزاد"]
        )

        loan_amount = st.number_input(
            "مبلغ درخواستی (ریال):",
            min_value=1_000_000,
            step=500_000,
            format="%i"
        )

        duration_months = st.number_input(
            "مدت بازپرداخت (ماه):",
            min_value=6,
            max_value=60,
            step=6
        )

        if st.button("📨 ثبت درخواست وام"):
            new_request = LoanRequest(
                customer_id=customer.id,
                loan_amount=loan_amount,
                loan_type=loan_type,
                duration_months=duration_months,
                request_date=date.today(),
                status="pending"
            )
            session.add(new_request)
            session.commit()
            st.success("✅ درخواست وام شما با موفقیت ثبت شد و در انتظار بررسی است.")

            # نمایش خلاصه‌ی درخواست
            st.info(
                f"نوع وام: {loan_type}\n\n"
                f"مبلغ: {loan_amount:,.0f} ریال\n\n"
                f"مدت بازپرداخت: {duration_months} ماه"
            )

    else:
        st.error("❌ اطلاعاتی با این کد ملی یافت نشد.")
        st.warning("لطفاً ابتدا برای افتتاح حساب به نزدیک‌ترین شعبه بانک مراجعه کنید.")
