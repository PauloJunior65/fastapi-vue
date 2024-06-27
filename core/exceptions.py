from typing import Any, Dict, List, Optional

from fastapi import HTTPException


def get_exception_route() -> Dict[int, Dict[str, str]]:
    """
    Retorna um dicionário contendo a rota para tratamento de exceções.
    """
    return {404: {'description': 'Não encontrado'}}


def add_error_field(field: str, message: str, error_type: str = '', errors: List[Dict[str, Any]] = []) -> List[Dict[str, Any]]:
    """
    Adiciona um campo de erro à lista de erros.
    """
    errors.append({'loc': (field,), 'msg': message, 'type': error_type})
    return errors


def create_field_exception(field: str, message: str, error_type: str = '', status_code: int = 422) -> HTTPException:
    """
    Cria uma HTTPException com um único erro de campo.
    """
    return HTTPException(status_code=status_code, detail=add_error_field(field, message, error_type))


def create_fields_exception(errors: List[Dict[str, Any]], status_code: int = 422) -> HTTPException:
    """
    Cria uma HTTPException com vários erros de campo.
    """
    return HTTPException(status_code=status_code, detail=errors)


def create_exception(message: str, status_code: int = 500, headers: Optional[Dict[str, Any]] = None) -> HTTPException:
    """
    Cria uma HTTPException com uma mensagem de erro geral.
    """
    return HTTPException(
        status_code=status_code,
        detail=message,
        headers=headers,
    )
