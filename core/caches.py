import pickle

import aioredis

from core.settings import get_settings

settings = get_settings()


def get_cache():
    """
    Retorna o cache padrão.
    """
    cache = Cache(url=settings.CACHE_URL)
    try:
        yield cache
    finally:
        cache._cache.close()


class CacheDepends:
    """
    Classe de dependência para o cache.
    """

    def __init__(self, db: int = None):
        self.db = db

    def __call__(self):
        url = settings.CACHE_URL
        if self.db is not None:
            url = f"{url}/{self.db}"
        cache = Cache(url=url)
        try:
            yield cache
        finally:
            cache._cache.close()


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

    @staticmethod
    def loads(data):
        try:
            return int(data)
        except ValueError:
            return pickle.loads(data)


class Cache:
    """
    Classe de cache.
    """

    def __init__(self, url: str):
        self._cache = aioredis.from_url(url, decode_responses=True)
        self._serializer = CacheSerializer()

    async def add(self, key: str, value, timeout: int = settings.CACHE_TIMEOUT):
        """Adiciona um valor ao cache

        Args:
            key (str): Cache key
            value (Any): Valor a ser adicionado
            timeout (int, optional): Tempo de expiração em segundos. Defaults to CACHE_TIMEOUT.

        Returns:
            bool: True se o valor foi adicionado, False caso contrário
        """
        value = self._serializer.dumps(value)
        return bool(await self._cache.set(key, value, ex=timeout, nx=True))

    async def get(self, key: str, default=None):
        """Retorna um valor do cache

        Args:
            key (str): Cache key
            default (Any, optional): Valor padrão. Defaults to None.

        Returns:
            Any: Valor do cache
        """
        value = await self._cache.get(key)
        return default if value is None else self._serializer.loads(value)

    async def set(self, key: str, value, timeout: int = settings.CACHE_TIMEOUT):
        """Adiciona ou atualiza um valor no cache

        Args:
            key (str): Cache key
            value (Any): Valor a ser adicionado ou atualizado
            timeout (int, optional): Tempo de expiração em segundos. Defaults to CACHE_TIMEOUT.
        """
        value = self._serializer.dumps(value)
        await self._cache.set(key, value, ex=timeout)

    async def get_or_set(self, key: str, default, timeout: int = settings.CACHE_TIMEOUT):
        """Retorna um valor do cache ou adiciona um valor padrão

        Args:
            key (str): Cache key
            default (Any): Valor padrão
            timeout (int, optional): Tempo de expiração em segundos. Defaults to CACHE_TIMEOUT.

        Returns:
            Any: Valor do cache
        """
        value = await self.get(key)
        if value is None:
            await self.set(key, default, timeout)
            return default
        return value

    async def touch(self, key: str, timeout: int = settings.CACHE_TIMEOUT):
        """Atualiza o tempo de expiração de um valor no cache

        Args:
            key (str): Cache key
            timeout (int, optional): Tempo de expiração em segundos. Defaults to CACHE_TIMEOUT.

        Returns:
            bool: True se o valor foi atualizado, False caso contrário
        """
        if timeout is None:
            return bool(await self._cache.persist(key))
        else:
            return bool(await self._cache.expire(key, timeout))

    async def delete(self, key: str):
        """Remove um valor do cache

        Args:
            key (str): Cache key

        Returns:
            bool: True se o valor foi removido, False caso contrário
        """
        return bool(await self._cache.delete(key))

    async def get_many(self, keys: list[str]):
        """Retorna vários valores do cache

        Args:
            keys (list[str]): Lista de chaves

        Returns:
            dict: Dicionário com os valores do cache
        """
        ret = await self._cache.mget(keys)
        return {k: self._serializer.loads(v) for k, v in zip(keys, ret) if v is not None}

    async def has_key(self, key: str):
        """Verifica se uma chave existe no cache

        Args:
            key (str): Cache key

        Returns:
            bool: True se a chave existe, False caso contrário
        """
        return bool(await self._cache.exists(key))

    async def incr(self, key: str, delta):
        """Incrementa um valor no cache

        Args:
            key (str): Cache key
            delta (Any): Valor a ser incrementado

        Raises:
            ValueError: Se a chave não existir

        Returns:
            Any: Valor incrementado
        """
        if not await self._cache.exists(key):
            raise ValueError("Key '%s' not found." % key)
        return await self._cache.incr(key, delta)

    async def set_many(self, data: dict, timeout: int = settings.CACHE_TIMEOUT):
        """Adiciona ou atualiza vários valores no cache

        Args:
            data (dict): Dicionário com os valores a serem adicionados ou atualizados
            timeout (int, optional): Tempo de expiração em segundos. Defaults to CACHE_TIMEOUT.
        """
        pipeline = self._cache.pipeline()
        await pipeline.mset({k: self._serializer.dumps(v) for k, v in data.items()})
        if timeout is not None:
            # Setting timeout for each key as redis does not support timeout
            # with mset().
            for key in data:
                await pipeline.expire(key, timeout)
        await pipeline.execute()

    async def delete_many(self, keys: list[str]):
        """Remove vários valores do cache

        Args:
            keys (list[str]): Lista de chaves
        """
        await self._cache.delete(*keys)

    async def clear(self):
        """Remove todos os valores do cache"""
        return bool(await self._cache.flushdb())
