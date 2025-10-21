import os
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Customer, Reviewer, LoanRequest, LoanReview, LoanDisbursement

# مسیر پایگاه داده
DATABASE_URL = "sqlite:///loan_management.db"

# ایجاد موتور اتصال به دیتابیس
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """ایجاد دیتابیس و افزودن داده‌های نمونه"""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    # ----------- Sample Data -----------

    # 1️⃣ مشتریان
    customers = [
        Customer(
            first_name="Amir",
            last_name="Hosseini",
            national_id="1234567890",
            phone_number="09120000001",
            email="amir.h@example.com",
            address="Tehran, Iran",
            account_number="ACC1001",
            account_balance=25000000,
            monthly_income=15000000,
            loan_history_count=2,
            loan_default_count=0,
            credit_score=720,
            employment_status="employed",
        ),
        Customer(
            first_name="Sara",
            last_name="Mohammadi",
            national_id="9876543210",
            phone_number="09123334455",
            email="sara.m@example.com",
            address="Isfahan, Iran",
            account_number="ACC1002",
            account_balance=12000000,
            monthly_income=8000000,
            loan_history_count=1,
            loan_default_count=1,
            credit_score=580,
            employment_status="employed",
        ),
    ]
    session.add_all(customers)
    session.commit()

    # 2️⃣ کارشناس بررسی وام
    reviewers = [
        Reviewer(
            first_name="Ali",
            last_name="Rezaei",
            employee_code="EMP001",
            position="Senior Credit Officer",
            branch_name="Tehran Central",
            email="ali.r@example.com"
        ),
        Reviewer(
            first_name="Maryam",
            last_name="Ahmadi",
            employee_code="EMP002",
            position="Loan Specialist",
            branch_name="Isfahan Branch",
            email="maryam.a@example.com"
        ),
    ]
    session.add_all(reviewers)
    session.commit()

    # 3️⃣ درخواست‌های وام
    loans = [
        LoanRequest(
            customer_id=1,
            loan_amount=50000000,
            loan_type="Personal",
            duration_months=24,
            request_date=datetime.date(2025, 10, 10),
            status="pending"
        ),
        LoanRequest(
            customer_id=2,
            loan_amount=20000000,
            loan_type="Car Loan",
            duration_months=18,
            request_date=datetime.date(2025, 10, 11),
            status="pending"
        ),
    ]
    session.add_all(loans)
    session.commit()

    # 4️⃣ بررسی‌ها (Loan Reviews)
    reviews = [
        LoanReview(
            loan_id=1,
            reviewer_id=1,
            review_date=datetime.date(2025, 10, 15),
            decision="approved",
            comments="Good credit score and sufficient income.",
            credit_score=720
        ),
        LoanReview(
            loan_id=2,
            reviewer_id=2,
            review_date=datetime.date(2025, 10, 16),
            decision="rejected",
            comments="Low credit score and poor repayment history.",
            credit_score=580
        ),
    ]
    session.add_all(reviews)
    session.commit()

    # 5️⃣ پرداخت وام (فقط برای وام تاییدشده)
    disbursements = [
        LoanDisbursement(
            loan_id=1,
            disbursement_date=datetime.date(2025, 10, 20),
            amount_paid=50000000,
            installment_count=24,
            installment_amount=2250000
        ),
    ]
    session.add_all(disbursements)
    session.commit()

    session.close()
    print("✅ Loan management database successfully created and populated with sample data.")


if __name__ == "__main__":
    if not os.path.exists("loan_management.db"):
        init_db()
    else:
        print("⚠️ The database 'loan_management.db' already exists.")
