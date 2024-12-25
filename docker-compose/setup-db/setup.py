from todo.models import TodoModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:example@todo-db/todos"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

results = db.query(TodoModel).all()

if len(results) == 0:
    print("No items found, creating default item")
    db.add(TodoModel(title="Default Todo", completed=False))
    db.commit()
else:
    print("Items found, skipping creation")

