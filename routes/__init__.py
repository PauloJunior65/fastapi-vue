import importlib
from pathlib import Path

from fastapi import APIRouter

from core.exceptions import get_exception_route

routers = APIRouter(
    tags=["main"],
    responses=get_exception_route(),
)

ignore_files = ['__init__.py']
for module_path in Path('routes').rglob('*.py'):
    if module_path.name in ignore_files:
        continue
    module_name = '.'.join(module_path.parts).removesuffix('.py')
    module = importlib.import_module(module_name)
    for obj_name in dir(module):
        obj = getattr(module, obj_name)
        if isinstance(obj, type) and issubclass(obj, APIRouter) and obj != APIRouter:
            routers.include_router(obj)
