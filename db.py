from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

# SQLite 使用時
# SQLite - File（通常のファイル保存）
engine = create_engine('sqlite:///sample_db.sqlite3')  # スラッシュは3本

# SQLログを表示したい場合には echo=True を指定
engine = create_engine('sqlite:///sample_db.sqlite3', echo=True)

# モデルの作成
# 説明のためファイル内に定義しますが、実際は別ファイル化して import します。

# まずベースモデルを生成します
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    age = Column(Integer)

    def __repr__(self):
        return "<User(id='%s', name='%s', age='%s')>" % (self.id, self.name, self.age)


# 次にベースモデルを継承してモデルクラスを定義します
class Student(Base):
    """
    生徒モデル
    必ず Base を継承
    """
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    score = Column(Integer)  # 点数

    def __repr__(self):
        return "<Student(id='%s', name='%s', score='%s')>" % (self.id, self.name, self.score)

#
# # テーブルの作成
# # テーブルがない場合 CREATE TABLE 文が実行される
Base.metadata.create_all(engine)  # 作成した engine を引数にすること

# SQLAlchemy はセッションを介してクエリを実行する
Session = sessionmaker(bind=engine)
session = Session()

session.add(User(id=1, name='Suzuki', age=21))

session.add_all([
    User(id=5, name='Yamada', age=39),
    User(id=7, name='Watanabe', age=88),
    User(id=10, name='Tanaka', age=15),
])

# コミット（データ追加を実行）
session.commit()

result = session.query(User).all()  # .all() は省略可
for user in result:
    print(user.name, user.age)

for user in session.query(User).filter(User.age > 20, User.age < 30):
    print(user.name)

# セッション・クローズ
# DB処理が不要になったタイミングやスクリプトの最後で実行
session.close()
