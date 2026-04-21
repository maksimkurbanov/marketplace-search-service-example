from src.application.ports.ad_source import AdSource
from src.application.ports.uow import UnitOfWork
from src.application.ports.usecases import IndexAdPort


class IndexAd(IndexAdPort):
    def __init__(self, uow: UnitOfWork, ad_source: AdSource) -> None:
        self._uow = uow
        self._ad_source = ad_source

    async def execute(self, ad_id: int) -> None:
        async with self._uow:
            ad = await self._ad_source.get(ad_id)
            if not ad or ad.status != "active":
                await self._uow.search.delete(ad_id)
                await self._uow.commit()
            else:
                await self._uow.search.upsert(
                    ad.ad_id,
                    ad.title,
                    ad.description,
                    ad.price,
                    ad.category,
                    ad.city,
                )
                await self._uow.commit()
