from sqlalchemy import Column, Integer, String
from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import nonebot


driver: nonebot.Driver = nonebot.get_driver()
config: nonebot.config.Config = driver.config


class AsyncEngine:
    def __init__(self, db_link):
        self.engine = create_async_engine(
            db_link,
            echo=False
        )


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


engine = AsyncORM(f"sqlite+aiosqlite:///{config.sqlite_host}")
Base = engine.Base


class Setu(Base):
    __tablename__ = "setu"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Group_id = Column(String(32))
    user_id = Column(Integer)
    image = Column(String(32))
    time = Column(Integer)

# engine = AsyncORM(f"sqlite:///warfarin.db")
# engine = create_engine(f"sqlite:///warfarin.db")
# engine = create_engine(f"sqlite:///{config.sqlite_host}")
# Setu.__table__.create(engine, checkfirst=True)
# DBSession = sessionmaker(bind=engine)
# session = DBSession()
#
# new_setu = Setu(id=0, Group_id=0, user_id=1, image="test", time=datetime.datetime.now())
# session.add(new_setu)
#
# session.commit()
# session.close()
