import importlib
from pathlib import Path

from sqlmodel import SQLModel

# Percorre todos os arquivos .py dentro do diretório "models" e subdiretórios
ignore_files = ['__init__.py']
for module_path in Path('models').rglob('*.py'):
    if module_path.name in ignore_files:
        continue
    module_name = '.'.join(module_path.parts).removesuffix('.py')
    module = importlib.import_module(module_name)
    for obj_name in dir(module):
        obj = getattr(module, obj_name)
        if isinstance(obj, type) and issubclass(obj, SQLModel) and obj != SQLModel:
            globals()[obj_name] = obj

# Remove as classes que não são filhas de SQLModel
for k, v in list(globals().items()):
    if isinstance(v, type) and issubclass(v, SQLModel):
        continue
    globals().pop(k)
del k, v
