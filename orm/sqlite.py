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

    async def insert_or_update(self, table, condition, dt):
        if (await self.execute(select(table).where(*condition))).all():
            return await self.execute(update(table).where(*condition).values(**dt))
        else:
            return await self.execute(insert(table).values(**dt))

    async def insert_or_ignore(self, table, condition, dt):
        if not (await self.execute(select(table).where(*condition))).all():
            return await self.execute(insert(table).values(**dt))

    async def delete(self, table, condition):
        return await self.execute(delete(table).where(*condition))

    async def init_check(self) -> bool:
        for table in Base.__subclasses__():
            try:
                await self.fetchone(select(table))
            except OperationalError:
                async with self.engine.begin() as conn:
                    await conn.run_sync(table.__table__.create(self.engine))
                return False
        return True

    async def search_sqlite_in_table_by_where(self, table_and_column, search_equation):
        """
        从表中搜索符合条件的数据
        table_and_column: 表名和表内的项目名，可填多个(Setu.Group_id, Setu.user_id, Setu.time etc.)
        search_equation: 搜索的条件,填写关系式，如(Setu.time > f"{datetime.date.now()}")
                         若需要填写多个关系式请用and_()连接；如and_(Setu.time > f"{datetime.date.today()}",
                                                           Setu.Group_id == f"{group_id}")
        """
        # today = datetime.date.today()
        # tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        # res = await self.engine.load_all(select(table_and_column).where(search_equation))
        return (await self.execute(select(table_and_column).where(search_equation))).fetchall()

    async def query_one(self, condition):
        """获取一个符合条件的数据
        如：await engine.query(func.max(ImageInformation.id))"""
        return (await self.execute(select(condition))).fetchone()

    async def query_count(self, condition):
        return (await self.execute(select(func.count(condition)))).fetchone()[0]

    async def select_distinct(self, table):
        stack = (await self.execute(select(table).distinct())).fetchall()
        res = []
        for result in stack:
            res.append(result[0])
        return res

engine = AsyncORM(f"sqlite+aiosqlite:///{config.sqlite_host}")
Base = engine.Base

