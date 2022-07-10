from typing import Union
from unittest import result
from sqlalchemy.orm import Session
import models
import schemas

# API Seller dashboard -----------------------------
def get_total_rows_order(db: Session, account_id: int):
    query = f"""SELECT COUNT(*) AS TOTAL_ROW_ORDER
                FROM account acc
                JOIN seller sl ON sl.account_id = acc.account_id
                JOIN `order` od ON od.seller_id = sl.seller_id
                WHERE (acc.account_id = {account_id}) """
    result = db.execute(query)
    return result.fetchall()