import importlib
from pathlib import Path

from sqlmodel import SQLModel

# Percorre todos os arquivos .py dentro do diretório "models" e subdiretórios
for module_path in Path('models').rglob('*.py'):
    if '__init__.py' in str(module_path):
        continue
    module_name = module_path.stem
    module = importlib.import_module(f'{module_name}' if __name__ == '__main__' else f'models.{module_name}')
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
