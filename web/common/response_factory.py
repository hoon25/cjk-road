# 응답 JSON FORM
def get_success_json(msg, data=None):
    """
    응답 성공 JSON 메세지
    :param msg:
    :param data:  default None
    :return:
    """
    if data is None:
        return {'result': 'success', 'msg': msg}
    else:
        return {'result': 'success', 'msg': msg, 'data': data}

def get_failure_json(msg):
    """
    응답 실패 JSON 메세지
    :param msg:
    :return:
    """
    return {'result': 'fail', 'msg': msg}