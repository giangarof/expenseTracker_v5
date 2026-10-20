from fastapi import FastAPI
from App.database.database import engine, Base
from App.routes.users import router as UserRoutes
from App.routes.expenses import router as ExpensesRoutes
from App.routes.income import router as IncomeRoutes
from App.routes.admin import router as AdminRoutes

app = FastAPI()
app.include_router(UserRoutes)
app.include_router(ExpensesRoutes)
app.include_router(IncomeRoutes)
app.include_router(AdminRoutes)

Base.metadata.create_all(bind=engine)
