from todo.models import TodoModel, Base
from sqlalchemy import create_engine
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:example@todo-db/todos"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)
