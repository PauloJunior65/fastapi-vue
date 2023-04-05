from .config import get_settings
import pickle
import redis

settings = get_settings()

def get_cache():
    """Default cache
    """
    db = RedisCache()
    try:
        yield db
    finally:
        db._cache.close()

class CacheCustom:
    """Custom cache
    """
    def __init__(self):
        pass

    def __call__(self, **kwars):
        db = RedisCache(**kwars)
        try:
            yield db
        finally:
            db._cache.close()


class RedisSerializer:
    """
    Serializer for redis cache.
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


class RedisCache:
    _cache: redis.Redis

    def __init__(self, **kwars):
        con = settings.redis()
        con.update(kwars)
        self._cache = redis.Redis(**con)
        self._serializer = RedisSerializer()

    def add(self, key: str, value, timeout:int=settings.REDIS_TIMEOUT):
        """Adiciona um valor ao cache

        Args:
            key (str): Cache key
            value (Any): Valor a ser adicionado
            timeout (int, optional): Tempo de expiração em segundos. Defaults to REDIS_TIMEOUT.

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

    def set(self, key:str, value, timeout:int=settings.REDIS_TIMEOUT):
        """Adiciona ou atualiza um valor no cache

        Args:
            key (str): Cache key
            value (Any): Valor a ser adicionado ou atualizado
            timeout (int, optional): Tempo de expiração em segundos. Defaults to REDIS_TIMEOUT.
        """
        value = self._serializer.dumps(value)
        self._cache.set(key, value, ex=timeout)

    def touch(self, key:str, timeout:int=settings.REDIS_TIMEOUT):
        """Atualiza o tempo de expiração de um valor no cache

        Args:
            key (str): Cache key
            timeout (int, optional): Tempo de expiração em segundos. Defaults to REDIS_TIMEOUT.

        Returns:
            bool: True se o valor foi atualizado, False caso contrário
        """
        if timeout is None:
            return bool(self._cache.persist(key))
        else:
            return bool(self._cache.expire(key, timeout))

    def delete(self, key:str):
        """Remove um valor do cache

        Args:
            key (str): Cache key

        Returns:
            bool: True se o valor foi removido, False caso contrário
        """
        return bool(self._cache.delete(key))

    def get_many(self, keys:list[str]):
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

    def has_key(self, key:str):
        """Verifica se uma chave existe no cache

        Args:
            key (str): Cache key

        Returns:
            bool: True se a chave existe, False caso contrário
        """
        return bool(self._cache.exists(key))

    def incr(self, key:str, delta):
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

    def set_many(self, data:dict, timeout:int=settings.REDIS_TIMEOUT):
        """Adiciona ou atualiza vários valores no cache

        Args:
            data (dict): Dicionário com os valores a serem adicionados ou atualizados
            timeout (int, optional): Tempo de expiração em segundos. Defaults to REDIS_TIMEOUT.
        """
        pipeline = self._cache.pipeline()
        pipeline.mset({k: self._serializer.dumps(v) for k, v in data.items()})
        if timeout is not None:
            # Setting timeout for each key as redis does not support timeout
            # with mset().
            for key in data:
                pipeline.expire(key, timeout)
        pipeline.execute()

    def delete_many(self, keys:list[str]):
        """Remove vários valores do cache

        Args:
            keys (list[str]): Lista de chaves
        """
        self._cache.delete(*keys)

    def clear(self):
        """Remove todos os valores do cache"""
        return bool(self._cache.flushdb())
