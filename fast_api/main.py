import logging
import os
import secrets
from logging.handlers import RotatingFileHandler
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import text
from starlette.requests import Request

from api.database import engine


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "api.log"

load_dotenv(BASE_DIR / ".env")
LOG_DIR.mkdir(parents=True, exist_ok=True)

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

if not ADMIN_USERNAME or not ADMIN_PASSWORD:
    raise RuntimeError(
        "ADMIN_USERNAME and ADMIN_PASSWORD must be set in .env"
    )


file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=2_000_000,
    backupCount=5,
    encoding="utf-8",
)

logger = logging.getLogger("ecommerce_api")
logger.setLevel(logging.INFO)
logger.handlers.clear()
logger.addHandler(file_handler)
logger.propagate = False

app = FastAPI(
    title="E-Commerce Data Warehouse API",
    description="API for the Olist e-commerce analytics project",
    version="1.0.0",
)

security = HTTPBasic()


def verify_admin(
    credentials: HTTPBasicCredentials = Depends(security),
):
    username_ok = secrets.compare_digest(
        credentials.username,
        ADMIN_USERNAME,
    )
    password_ok = secrets.compare_digest(
        credentials.password,
        ADMIN_PASSWORD,
    )

    if not (username_ok and password_ok):
        raise HTTPException(
            status_code=401,
            detail="Invalid administrator credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        response = await call_next(request)

        if response.status_code >= 500:
            logger.error(
                "HTTP %s | %s %s",
                response.status_code,
                request.method,
                request.url.path,
            )

        return response

    except Exception:
        logger.exception(
            "Unhandled exception | %s %s",
            request.method,
            request.url.path,
        )
        raise


@app.get("/", response_class=HTMLResponse)
def home(admin: str = Depends(verify_admin)):
    return """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>E-Commerce | Data Platform</title>
        <style>
            * { box-sizing: border-box; }

            body {
                margin: 0;
                background: #0b1120;
                color: #e5edf8;
                font-family: Tahoma, Arial, sans-serif;
                line-height: 1.8;
            }

            a { color: inherit; text-decoration: none; }

            .container {
                max-width: 1120px;
                margin: auto;
                padding: 32px 22px 50px;
            }

            .topbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 16px;
                padding-bottom: 24px;
                border-bottom: 1px solid #263248;
            }

            .brand {
                display: flex;
                align-items: center;
                gap: 12px;
                font-size: 16px;
                font-weight: bold;
            }

            .logo {
                display: grid;
                place-items: center;
                width: 44px;
                height: 44px;
                border-radius: 13px;
                background: linear-gradient(135deg, #38bdf8, #6366f1);
                color: white;
                font-size: 21px;
            }

            .status {
                color: #86efac;
                background: #123126;
                border: 1px solid #22543d;
                border-radius: 30px;
                padding: 6px 12px;
                font-size: 12px;
                white-space: nowrap;
            }

            .hero {
                margin: 42px 0 32px;
                padding: 34px;
                border: 1px solid #293750;
                border-radius: 24px;
                background:
                    radial-gradient(ellipse at top left,
                    rgba(56,189,248,.15), transparent 55%),
                    linear-gradient(135deg, #151f33, #101827);
            }

            .eyebrow {
                color: #7dd3fc;
                font-size: 12px;
                letter-spacing: 1px;
            }

            h1 {
                margin: 10px 0;
                font-size: clamp(25px, 4vw, 38px);
                line-height: 1.5;
            }

            .hero p {
                color: #a8b6ca;
                max-width: 680px;
                margin-bottom: 0;
            }

            .section-heading {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin: 32px 0 18px;
            }

            h2 {
                font-size: 19px;
                margin: 0;
            }

            .muted {
                color: #8493aa;
                font-size: 12px;
            }

            .grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 18px;
            }

            .card {
                position: relative;
                display: block;
                padding: 24px;
                min-height: 195px;
                overflow: hidden;
                background: #121c2d;
                border: 1px solid #28364d;
                border-radius: 18px;
                transition: .2s ease;
            }

            .card:hover {
                transform: translateY(-4px);
                border-color: #38bdf8;
                background: #17253a;
            }

            .icon {
                display: grid;
                place-items: center;
                width: 48px;
                height: 48px;
                border-radius: 14px;
                margin-bottom: 15px;
                font-size: 23px;
            }

.blue { background: #15354d; }
            .purple { background: #30264f; }
            .green { background: #153b35; }
            .orange { background: #49301f; }

            .card h3 {
                margin: 0 0 5px;
                font-size: 17px;
            }

            .card p {
                margin: 0;
                color: #9cabc0;
                font-size: 13px;
            }

            .card .open {
                display: inline-block;
                margin-top: 16px;
                color: #7dd3fc;
                font-size: 12px;
            }

            .bottom {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                gap: 12px;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #263248;
                color: #8493aa;
                font-size: 12px;
            }

            @media (max-width: 650px) {
                .container { padding: 20px 14px 35px; }
                .hero { padding: 23px; margin-top: 26px; }
                .grid { grid-template-columns: 1fr; }
                .topbar { align-items: flex-start; }
                .brand { font-size: 13px; }
                .status { font-size: 10px; }
                .card { min-height: auto; }
            }
        </style>
    </head>
    <body>
        <main class="container">
            <header class="topbar">
                <div class="brand">
                    <div class="logo">◈</div>
                    <div>
                        <div>E-Commerce Data Platform</div>
                        <div class="muted">DATA WAREHOUSE & BI</div>
                    </div>
                </div>
                <div class="status">● دسترسی مدیر فعال است</div>
            </header>

            <section class="hero">
                <div class="eyebrow">ADMINISTRATION / OVERVIEW</div>
                <h1>پنل مدیریت انبار داده</h1>
                <p>
                    به پنل پروژه تجارت الکترونیک خوش آمدی.
                    از اینجا می‌توانی وضعیت سرویس را بررسی کنی،
                    ساختار دیتابیس را ببینی و نتایج کنترل کیفیت داده‌ها را مرور کنی.
                </p>
            </section>

            <div class="section-heading">
                <h2>ابزارهای پروژه</h2>
                <span class="muted">۴ بخش قابل دسترسی</span>
            </div>

            <section class="grid">
                <a class="card" href="/health">
                    <div class="icon green">✓</div>
                    <h3>وضعیت API</h3>
                    <p>بررسی فعال بودن سرویس و پاسخ‌گویی آن.</p>
                    <span class="open">بررسی وضعیت ←</span>
                </a>

                <a class="card" href="/database/tables">
                    <div class="icon blue">▦</div>
                    <h3>جداول دیتابیس</h3>
                    <p>مشاهده نام جدول‌ها و Schemaهای موجود در SQL Server.</p>
                    <span class="open">مشاهده جدول‌ها ←</span>
                </a>

                <a class="card" href="/database/columns">
                    <div class="icon purple">▤</div>
                    <h3>ساختار انبار داده</h3>
                    <p>بررسی ستون‌ها، نوع داده و وضعیت NULL در جداول dw.</p>
                    <span class="open">مشاهده ستون‌ها ←</span>
                </a>

                <a class="card" href="/admin/logs">
                    <div class="icon orange">≋</div>
                    <h3>لاگ کنترل کیفیت</h3>
                    <p>مشاهده رکوردهای PASS و REVIEW ذخیره‌شده در SQL Server.</p>
                    <span class="open">مشاهده لاگ‌ها ←</span>
                </a>
            </section>

            <footer class="bottom">
                <span>Olist E-Commerce Data Warehouse Project</span>
                <span>FastAPI · SQL Server · Data Quality</span>
            </footer>
        </main>
    </body>
    </html>
    """
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "E-Commerce API is running",
    }


@app.get("/database/tables")
def list_database_tables():
    query = text("""
        SELECT
            s.name AS schema_name,
            t.name AS table_name
        FROM sys.tables AS t
        INNER JOIN sys.schemas AS s
            ON t.schema_id = s.schema_id
        ORDER BY s.name, t.name;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        tables = [
            {"schema": row.schema_name, "table": row.table_name}
            for row in result
        ]

    return {"tables": tables}

@app.get("/database/columns")
def list_database_columns():
    query = text("""
        SELECT
            s.name AS schema_name,
            t.name AS table_name,
            c.name AS column_name,
            ty.name AS data_type,
            c.is_nullable
        FROM sys.tables AS t
        INNER JOIN sys.schemas AS s
            ON t.schema_id = s.schema_id
        INNER JOIN sys.columns AS c
            ON t.object_id = c.object_id
        INNER JOIN sys.types AS ty
            ON c.user_type_id = ty.user_type_id
        WHERE s.name = 'dw'
        ORDER BY t.name, c.column_id;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        columns = [
            {
                "schema": row.schema_name,
                "table": row.table_name,
                "column": row.column_name,
                "data_type": row.data_type,
                "nullable": bool(row.is_nullable),
            }
            for row in result
        ]

    return {"columns": columns}


@app.get("/admin/logs")
def view_quality_logs(
    admin: str = Depends(verify_admin),
    limit: int = Query(default=200, ge=1, le=2000),
):
    query = text("""
        SELECT TOP (:limit) *
        FROM dbo.DataQualityLog
        ORDER BY 1 DESC;
    """)

    try:
        with engine.connect() as connection:
            result = connection.execute(
                query,
                {"limit": limit},
            )
            rows = [dict(row._mapping) for row in result]

        return {
            "source": "dbo.DataQualityLog",
            "count": len(rows),
            "logs": rows,
        }

    except Exception:
        logger.exception("Failed to retrieve data quality logs")
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve data quality logs",
        )