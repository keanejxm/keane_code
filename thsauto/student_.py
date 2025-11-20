#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-09-12 0:35
# @Author  : keane
# @Site    : 
# @File    : student_.py
# @Software: PyCharm
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from datetime import datetime, date
from route_.auth_ import get_current_user
from config_.mysql_utils import MySQLUtils
from config_.config import mysql_config
from route_.auth_ import ResValue

router = APIRouter()


class BaseInfo(BaseModel):
    userId: str
    phoneNumber: str
    serverStartDt: datetime
    serverEndDt: datetime
    groupType: int
    # serverData: str
    roleType: int


class AddTradeAccount(BaseModel):
    tradeAccount: str
    tradePassword: str


class AccountData(BaseModel):
    id: Optional[int] = None
    userId: str
    tradeAccount: str  # 交易账户
    tradePassword: str  # 交易密码
    cashBalance: str  # 现金余额
    positionTotal: str  # 持仓总金额


class TradeAccount(BaseModel):
    cashBalance: float
    positionTotal: float


@router.post("/base_info", response_model=BaseInfo)
async def student_data(current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not logged in",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = current_user.userId
    sql = f"select * from users  where userId='{user_id}'"
    db = MySQLUtils(**mysql_config)
    user_data = db.search(sql)
    baseInfo = BaseInfo(**user_data[0])
    return baseInfo


@router.post("/add_account", response_model=ResValue)
def add_account(tradeInfo: AddTradeAccount, current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not logged in",
            headers={"WWW-Authenticate": "Bearer"},
        )
    new_account = AccountData(
        userId=current_user.userId,
        tradeAccount=tradeInfo.tradeAccount,
        tradePassword=tradeInfo.tradePassword,
        cashBalance="100000",
        positionTotal="101000",
    )
    account_dict = new_account.model_dump()
    account_dict["createdDt"] = datetime.now()
    account_dict["updatedDt"] = datetime.now()
    db = MySQLUtils(**mysql_config)
    res_id = db.insert("trade_account_info", account_dict)
    return dict(code=1, msg="ok", data={"tradeId": res_id})


@router.post("/trade_account", response_model=ResValue)
async def trade_account(current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not logged in",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # sql查询数据
    db = MySQLUtils(**mysql_config)
    sql = "select * from trade_account_info where userId='{user_id}'".format(user_id=current_user.userId)
    res = db.search(sql)
    account_data = TradeAccount(**res[0])
    return dict(code=1, msg="ok",
                data=dict(cashBalance=account_data.cashBalance, positionTotal=account_data.positionTotal))
