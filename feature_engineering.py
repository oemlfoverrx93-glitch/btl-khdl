import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Float, Integer
from sklearn.preprocessing import StandardScaler

# =========================
# KẾT NỐI SQL SERVER
# =========================

server = 'NGAN-NGUYEN'
database = 'HousePrices'

connection_string = (
    f"mssql+pyodbc://@{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

engine = create_engine(connection_string)
# =========================
# LẤY DỮ LIỆU TỪ SQL SERVER
# =========================

query = """
SELECT
    OverallQual,
    GrLivArea,
    GarageCars,
    TotalBsmtSF,
    FullBath,
    YearBuilt,
    LotArea,
    BedroomAbvGr,
    TotRmsAbvGrd,
    GarageArea,
    SalePrice
FROM houses_train
WHERE SalePrice > 0
"""

df = pd.read_sql(query, engine)

# =========================
# HIỂN THỊ DỮ LIỆU
# =========================

print("5 dòng đầu của dữ liệu:")
print(df.head())

# =========================
# KIỂM TRA DỮ LIỆU THIẾU
# =========================

print("\nSố lượng missing values:")
print(df.isnull().sum())

# =========================
# XÓA DỮ LIỆU THIẾU
# =========================

df = df.dropna()

# =========================
# CHUẨN HÓA DỮ LIỆU
# =========================

feature_cols = [
    'OverallQual',
    'GrLivArea',
    'GarageCars',
    'TotalBsmtSF',
    'FullBath',
    'YearBuilt',
    'LotArea',
    'BedroomAbvGr',
    'TotRmsAbvGrd',
    'GarageArea'
]

scaler = StandardScaler()

df[feature_cols] = scaler.fit_transform(df[feature_cols])

# =========================
# HIỂN THỊ SAU KHI SCALE
# =========================

print("\nDữ liệu sau khi chuẩn hóa:")
print(df.head())

# =========================
# XUẤT FILE CSV
# =========================

df.to_csv("clean_house_data.csv", index=False)

print("\nĐã tạo file clean_house_data.csv")

# =========================
# ĐẨY DỮ LIỆU LÊN SQL SERVER
# =========================

df.to_sql(
    'clean_houses_train',
    engine,
    if_exists='replace',
    index=False,
    dtype={
        'OverallQual': Float(),
        'GrLivArea': Float(),
        'GarageCars': Float(),
        'TotalBsmtSF': Float(),
        'FullBath': Float(),
        'YearBuilt': Float(),
        'LotArea': Float(),
        'BedroomAbvGr': Float(),
        'TotRmsAbvGrd': Float(),
        'GarageArea': Float(),
        'SalePrice': Integer()
    }
)

print("\nĐã đẩy dữ liệu lên SQL Server thành công!")