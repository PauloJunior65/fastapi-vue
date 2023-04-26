from fastapi import HTTPException
from fastapi_babel import _

responses = {
    404: {"description": _("Not found")}
}


def add_error(campo: str, mensagem: str, tipo: str = '', errors: list = []):
    errors.append({'loc': (campo,), 'msg': mensagem, 'type': tipo})
    return errors


def exception_field(campo: str, mensagem: str, tipo: str = '', status_code=422):
    raise HTTPException(status_code=status_code,
                        detail=add_error(campo, mensagem, tipo))


def exception_fields(errors: list, status_code=422):
    raise HTTPException(status_code=status_code, detail=errors)


def exception(mensagem: str, status_code=500, headers: dict = None):
    raise HTTPException(
        status_code=status_code,
        detail=mensagem,
        headers=headers,
    )
