import nonebot
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

driver: nonebot.Driver = nonebot.get_driver()
config: nonebot.config.Config = driver.config


class AsyncEngine:
    def __init__(self, db_link):
        self.engine = create_async_engine(
            db_link,
            echo=False
        )

    async def execute(self, sql, **kwargs):
        async with AsyncSession(self.engine) as session:
            try:
                result = await session.execute(sql, **kwargs)
                await session.commit()
                return result
            except Exception as e:
                await session.rollback()
                raise e


class AsyncORM(AsyncEngine):
    def __init__(self, conn):
        super().__init__(conn)
        self.session = AsyncSession(bind=self.engine)
        self.Base = declarative_base(self.engine)
        self.async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def create_all(self):
        """创建所有表"""
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)

    async def drop_all(self):
        """删除所有表"""
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.drop_all)

    async def add(self, table, dt):
        """添加信息"""
        async with self.async_session() as session:
            async with session.begin():
                session.add(table(**dt), _warn=False)
            await session.commit()

    async def load_all(self, sql):
        """查询信息
        sql: 查询指令
        例： engine.load_all(select(Setu.user_id, Setu.time).where(Setu.time > f"{datetime.date.today()}"))"""
        return (await self.execute(sql)).fetchall()


engine = AsyncORM(f"sqlite+aiosqlite:///{config.sqlite_host}")
Base = engine.Base

