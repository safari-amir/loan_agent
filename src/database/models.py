from sqlalchemy import Column, Integer, String, Date, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


# =========================
# 1️⃣ جدول مشتری (Customer)
# =========================
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    national_id = Column(String, unique=True, index=True)
    phone_number = Column(String)
    email = Column(String, unique=True)
    address = Column(String)
    account_number = Column(String, unique=True)
    account_balance = Column(DECIMAL(12, 2), default=0)
    monthly_income = Column(DECIMAL(12, 2))
    loan_history_count = Column(Integer, default=0)
    loan_default_count = Column(Integer, default=0)
    credit_score = Column(Integer)
    employment_status = Column(String)  # e.g. employed / unemployed / retired ...


    # رابطه با درخواست‌های وام
    loans = relationship("LoanRequest", back_populates="customer")


# =================================
# 2️⃣ جدول کارشناس بررسی وام (Reviewer)
# =================================
class Reviewer(Base):
    __tablename__ = "reviewers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    employee_code = Column(String, unique=True, index=True)
    position = Column(String)
    branch_name = Column(String)
    email = Column(String, unique=True)

    reviews = relationship("LoanReview", back_populates="reviewer")
    approved_loans = relationship("LoanRequest", back_populates="reviewer")


# ==================================
# 3️⃣ جدول درخواست وام (LoanRequest)
# ==================================
class LoanRequest(Base):
    __tablename__ = "loan_requests"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    loan_amount = Column(DECIMAL(12, 2))
    loan_type = Column(String)
    duration_months = Column(Integer)
    request_date = Column(Date)
    status = Column(String, default="pending")  # pending / approved / rejected
    reviewer_id = Column(Integer, ForeignKey("reviewers.id"), nullable=True)

    customer = relationship("Customer", back_populates="loans")
    reviewer = relationship("Reviewer", back_populates="approved_loans")
    reviews = relationship("LoanReview", back_populates="loan")
    disbursement = relationship("LoanDisbursement", back_populates="loan", uselist=False)


# =================================
# 4️⃣ جدول بررسی درخواست (LoanReview)
# =================================
class LoanReview(Base):
    __tablename__ = "loan_reviews"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loan_requests.id"))
    reviewer_id = Column(Integer, ForeignKey("reviewers.id"))
    review_date = Column(Date)
    decision = Column(String)  # approved / rejected
    comments = Column(String)
    credit_score = Column(Integer)

    loan = relationship("LoanRequest", back_populates="reviews")
    reviewer = relationship("Reviewer", back_populates="reviews")


# ====================================
# 5️⃣ جدول پرداخت وام (LoanDisbursement)
# ====================================
class LoanDisbursement(Base):
    __tablename__ = "loan_disbursements"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loan_requests.id"))
    disbursement_date = Column(Date)
    amount_paid = Column(DECIMAL(12, 2))
    installment_count = Column(Integer)
    installment_amount = Column(DECIMAL(12, 2))

    loan = relationship("LoanRequest", back_populates="disbursement")
