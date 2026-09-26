from fastapi import FastAPI
from App.database.database import engine, Base
from App.routes.users import router as UserRoutes
from App.routes.expenses import router as ExpensesRoutes

app = FastAPI()
app.include_router(UserRoutes)
app.include_router(ExpensesRoutes)

Base.metadata.create_all(bind=engine)
