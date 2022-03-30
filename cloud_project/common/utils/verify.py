# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : utils_verify.py
# @Software: PyCharm

"""
公共方法
"""
import string
import random
import traceback

from ronglian_sms_sdk import SmsSDK



from flask import Blueprint, make_response
from common.utils.captcha import Captcha
from common.models import cache


# accId = '8aaf07087f77bf96017fd54021082f71'
# accToken = 'fcc9d94e2c324d32a93081fe8323c959'
# appId = '8aaf07087f77bf96017fd54021ff2f78'

accId = '8a216da87de15752017dfedb7d6c05fd'
accToken = '24018819bfea4d8d8cbe9f57e2b5baab'
appId = '8aaf07087de13e49017dffb4a95106d4'


def generate_code():
    return Captcha.gene_graph_captcha()


def phone_code(mobile, code):
    """
    短信验证码功能
    :return:
    """
    sdk = SmsSDK(accId, accToken, appId)
    datas = (code, '5')
    resp = sdk.sendMessage('1', mobile, datas)
    return resp
