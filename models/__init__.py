from sqlalchemy import MetaData
import importlib
import glob

Base = MetaData()

for module in glob.glob('models/**/*.py', recursive=True):
    if '__init__.py' in module: continue
    module = importlib.import_module(module.removesuffix('.py').replace('\\','.').replace('/','.'))
    if hasattr(module, 'Base'):
        for (table_name, table) in module.Base.metadata.tables.items():
            Base._add_table(table_name, table.schema, table)