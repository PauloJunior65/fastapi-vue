# import importlib
# import sys
# from pathlib import Path

# from sqlalchemy.orm import registry

# table_registry = registry()

# # Percorre todos os arquivos .py dentro do diretório "models" e subdiretórios
# for module_path in Path('models').rglob('*.py'):
#     if '__init__.py' in str(module_path):
#         continue
#     module_name = module_path.stem

#     # Verifica se o módulo já foi importado anteriormente
#     if module_name in sys.modules:
#         continue

#     # Carrega o módulo
#     module = importlib.import_module(f'models.{module_name}')

#     # Verifica se o módulo possui um objeto "table_registry" e adiciona ao registro principal
#     if hasattr(module, 'table_registry') and isinstance(module.table_registry, registry):
#         table_registry.add_registry(module.table_registry)
