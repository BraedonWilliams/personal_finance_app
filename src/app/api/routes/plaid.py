""" from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from plaid import Client
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from datetime import datetime, timedelta

from src.app.db.database import get_db
from src.app.api.schemas.plaid import (
    PlaidPublicToken,
    PlaidLinkToken,
    AccountList,
    AccountBase,
    TransactionList,
    TransactionBase,
)

# -------------------------
# PLAID CONFIG
# -------------------------

PLAID_CLIENT_ID = "YOUR_CLIENT_ID"
PLAID_SECRET = "YOUR_SECRET"
PLAID_ENV = "sandbox"  # or "development" / "production"

configuration = plaid_api.Configuration(
    host=plaid_api.Environment.Sandbox,
    api_key={
        "clientId": PLAID_CLIENT_ID,
        "secret": PLAID_SECRET
    }
)

api_client = plaid_api.ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)

router = APIRouter(prefix="/plaid", tags=["Plaid"])

# -------------------------
# 1️⃣ CREATE LINK TOKEN
# -------------------------

@router.post("/link-token", response_model=PlaidLinkToken)
def create_link_token(db: Session = Depends(get_db)):
    request = LinkTokenCreateRequest(
        products=["auth", "transactions"],
        client_name="Personal Finance App",
        language="en",
        country_codes=["US"],
        user=LinkTokenCreateRequestUser(client_user_id="test_user"),
    )

    response = plaid_client.link_token_create(request)
    return {"link_token": response.link_token}


# -------------------------
# 2️⃣ EXCHANGE PUBLIC TOKEN → ACCESS TOKEN
# -------------------------

@router.post("/exchange-token")
def exchange_public_token(payload: PlaidPublicToken):
    request = ItemPublicTokenExchangeRequest(
        public_token=payload.public_token
    )
    response = plaid_client.item_public_token_exchange(request)

    # In real app you save access_token to DB
    access_token = response.access_token 

    return {"access_token": access_token}


# -------------------------
# 3️⃣ GET BANK ACCOUNTS
# -------------------------

@router.get("/accounts", response_model=AccountList)
def get_accounts(access_token: str):
    request = AccountsGetRequest(access_token=access_token)
    response = plaid_client.accounts_get(request)

    accounts = [
        AccountBase(
            account_id=a.account_id,
            name=a.name,
            official_name=a.official_name,
            type=a.type,
            subtype=a.subtype,
            mask=a.mask,
            current_balance=a.balances.current,
            available_balance=a.balances.available,
        ) for a in response.accounts
    ]

    return {"accounts": accounts}


# -------------------------
# 4️⃣ GET TRANSACTIONS
# -------------------------

@router.get("/transactions", response_model=TransactionList)
def get_transactions(access_token: str):
    start_date = (datetime.now() - timedelta(days=30)).date()
    end_date = datetime.now().date()

    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=start_date,
        end_date=end_date,
    )

    response = plaid_client.transactions_get(request)

    transactions = [
        TransactionBase(
            transaction_id=t.transaction_id,
            date=t.date,
            name=t.name,
            amount=t.amount,
            account_id=t.account_id,
            category=t.category,
            pending=t.pending,
        ) for t in response.transactions
    ]

    return {"transactions": transactions}
 """