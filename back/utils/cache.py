from .config import get_settings
import pickle
import redis

settings = get_settings()


def _hidrate_cache(host: str = "127.0.0.1", port: int = 6379, username: str = None, password: str = None, db: int = 1):
    if username or password:
        return {
            'host': host,
            'port': port,
            'username': username if username else 'default',
            'password': password,
            'db': db
        }
    else:
        return {
            'host': host,
            'port': port,
            'db': db
        }

_caches = {k: _hidrate_cache(**v) for k, v in settings.caches.items()}


def get_cache():
    """Cache padrão"""
    db = _caches.get("default")
    if db is None:
        raise ValueError("Cache default not found")
    db = Cache(**db)
    try:
        yield db
    finally:
        db._cache.close()


class CacheCustom:
    """Cache personalizado"""

    def __init__(self, con:str='default', db: int = None):
        """Cache personalizado

        Args:
            con (str, optional): Nome da conexão. Defaults to 'default'.
            db (int, optional): Banco de dados.
        """
        self.con = _caches.get(con,{}).copy()
        if not self.con:
            raise ValueError(f"Cache {con} not found")
        if db is not None:
            self.con['db'] = db

    def __call__(self):
        db = Cache(**self.con)
        try:
            yield db
        finally:
            db._cache.close()


class CacheSerializer:
    """
    Serializador de dados para o cache.
    """

    def __init__(self, protocol=None):
        self.protocol = pickle.HIGHEST_PROTOCOL if protocol is None else protocol

    def dumps(self, obj):
        # Only skip pickling for integers, a int subclasses as bool should be
        # pickled.
        if type(obj) is int:
            return obj
        return pickle.dumps(obj, self.protocol)

    def loads(self, data):
        try:
            return int(data)
        except ValueError:
            return pickle.loads(data)


class Cache:
    _cache: redis.Redis

    def __init__(self, **kwars):
        self._cache = redis.Redis(**kwars)
        self._serializer = CacheSerializer()

    def add(self, key: str, value, timeout: int = settings.CACHE_TIMEOUT):
        """Adiciona um valor ao cache

        Args:
            key (str): Cache key
            value (Any): Valor a ser adicionado
            timeout (int, optional): Tempo de expiração em segundos. Defaults to CACHE_TIMEOUT.

        Returns:
            bool: True se o valor foi adicionado, False caso contrário
        """
        value = self._serializer.dumps(value)
        return bool(self._cache.set(key, value, ex=timeout, nx=True))

    def get(self, key: str, default=None):
        """Retorna um valor do cache

        Args:
            key (str): Cache key
            default (Any, optional): Valor padrão. Defaults to None.

        Returns:
            Any: Valor do cache
        """
        value = self._cache.get(key)
        return default if value is None else self._serializer.loads(value)

    def set(self, key: str, value, timeout: int = settings.CACHE_TIMEOUT):
        """Adiciona ou atualiza um valor no cache

        Args:
            key (str): Cache key
            value (Any): Valor a ser adicionado ou atualizado
            timeout (int, optional): Tempo de expiração em segundos. Defaults to CACHE_TIMEOUT.
        """
        value = self._serializer.dumps(value)
        self._cache.set(key, value, ex=timeout)

    def get_or_set(self, key: str, default, timeout: int = settings.CACHE_TIMEOUT):
        """Retorna um valor do cache ou adiciona um valor padrão

        Args:
            key (str): Cache key
            default (Any): Valor padrão
            timeout (int, optional): Tempo de expiração em segundos. Defaults to CACHE_TIMEOUT.

        Returns:
            Any: Valor do cache
        """
        value = self.get(key)
        if value is None:
            self.set(key, default, timeout)
            return default
        return value

    def touch(self, key: str, timeout: int = settings.CACHE_TIMEOUT):
        """Atualiza o tempo de expiração de um valor no cache

        Args:
            key (str): Cache key
            timeout (int, optional): Tempo de expiração em segundos. Defaults to CACHE_TIMEOUT.

        Returns:
            bool: True se o valor foi atualizado, False caso contrário
        """
        if timeout is None:
            return bool(self._cache.persist(key))
        else:
            return bool(self._cache.expire(key, timeout))

    def delete(self, key: str):
        """Remove um valor do cache

        Args:
            key (str): Cache key

        Returns:
            bool: True se o valor foi removido, False caso contrário
        """
        return bool(self._cache.delete(key))

    def get_many(self, keys: list[str]):
        """Retorna vários valores do cache

        Args:
            keys (list[str]): Lista de chaves

        Returns:
            dict: Dicionário com os valores do cache
        """
        ret = self._cache.mget(keys)
        return {
            k: self._serializer.loads(v) for k, v in zip(keys, ret) if v is not None
        }

    def has_key(self, key: str):
        """Verifica se uma chave existe no cache

        Args:
            key (str): Cache key

        Returns:
            bool: True se a chave existe, False caso contrário
        """
        return bool(self._cache.exists(key))

    def incr(self, key: str, delta):
        """Incrementa um valor no cache

        Args:
            key (str): Cache key
            delta (Any): Valor a ser incrementado

        Raises:
            ValueError: Se a chave não existir

        Returns:
            Any: Valor incrementado
        """
        if not self._cache.exists(key):
            raise ValueError("Key '%s' not found." % key)
        return self._cache.incr(key, delta)

    def set_many(self, data: dict, timeout: int = settings.CACHE_TIMEOUT):
        """Adiciona ou atualiza vários valores no cache

        Args:
            data (dict): Dicionário com os valores a serem adicionados ou atualizados
            timeout (int, optional): Tempo de expiração em segundos. Defaults to CACHE_TIMEOUT.
        """
        pipeline = self._cache.pipeline()
        pipeline.mset({k: self._serializer.dumps(v) for k, v in data.items()})
        if timeout is not None:
            # Setting timeout for each key as redis does not support timeout
            # with mset().
            for key in data:
                pipeline.expire(key, timeout)
        pipeline.execute()

    def delete_many(self, keys: list[str]):
        """Remove vários valores do cache

        Args:
            keys (list[str]): Lista de chaves
        """
        self._cache.delete(*keys)

    def clear(self):
        """Remove todos os valores do cache"""
        return bool(self._cache.flushdb())
