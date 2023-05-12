from fastapi import FastAPI
import importlib
import glob


def add_routers(app: FastAPI):
    for module in glob.glob('modules/**/*.py', recursive=True):
        if '__init__.py' in module:
            continue
        module = importlib.import_module(module.removesuffix(
            '.py').replace('\\', '.').replace('/', '.'))
        if hasattr(module, 'router'):
            app.include_router(module.router)
