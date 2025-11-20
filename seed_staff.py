import os
import uuid
import datetime

import bcrypt
import boto3

DYNAMO_REGION = "us-east-1"
TABLE_NAME = "Staff"

TENANTS = [
    "tenant_pq_barranco",      # Sede Barranco (UTEC)
    "tenant_pq_puruchuco",     # Sede Puruchuco
    "tenant_pq_villamaria",    # Sede Villa María
    "tenant_pq_jiron",         # Sede Jirón
]

STAFF_PER_TENANT = [
    # 2 admins
    {
        "id_staff_suffix": "admin1",
        "name": "Administrador 1",
        "dni": "80000001",
        "role": "admin",
        "email_suffix": "admin1",
        "phone": "+51 900000001",
        "status": "activo",
    },
    {
        "id_staff_suffix": "admin2",
        "name": "Administrador 2",
        "dni": "80000002",
        "role": "admin",
        "email_suffix": "admin2",
        "phone": "+51 900000002",
        "status": "activo",
    },
    # 3 staff (cocina/mostrador)
    {
        "id_staff_suffix": "staff1",
        "name": "Staff 1",
        "dni": "70000001",
        "role": "staff",
        "email_suffix": "staff1",
        "phone": "+51 900000101",
        "status": "activo",
    },
    {
        "id_staff_suffix": "staff2",
        "name": "Staff 2",
        "dni": "70000002",
        "role": "staff",
        "email_suffix": "staff2",
        "phone": "+51 900000102",
        "status": "activo",
    },
    {
        "id_staff_suffix": "staff3",
        "name": "Staff 3",
        "dni": "70000003",
        "role": "staff",
        "email_suffix": "staff3",
        "phone": "+51 900000103",
        "status": "activo",
    },
    # 3 delivery
    {
        "id_staff_suffix": "delivery1",
        "name": "Repartidor 1",
        "dni": "60000001",
        "role": "delivery",
        "email_suffix": "delivery1",
        "phone": "+51 900000201",
        "status": "activo",
    },
    {
        "id_staff_suffix": "delivery2",
        "name": "Repartidor 2",
        "dni": "60000002",
        "role": "delivery",
        "email_suffix": "delivery2",
        "phone": "+51 900000202",
        "status": "activo",
    },
    {
        "id_staff_suffix": "delivery3",
        "name": "Repartidor 3",
        "dni": "60000003",
        "role": "delivery",
        "email_suffix": "delivery3",
        "phone": "+51 900000203",
        "status": "activo",
    },
]


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def main():
    session = boto3.Session(region_name=DYNAMO_REGION)
    dynamo = session.resource("dynamodb")
    table = dynamo.Table(TABLE_NAME)

    # Password fijo para todos los usuarios seed: 123456
    default_password = "123456"
    password_h = hash_password(default_password)

    now = datetime.datetime.utcnow().isoformat()

    for tenant in TENANTS:
        # usar el sufijo del tenant como id_sucursal simple
        id_sucursal = tenant.replace("tenant_", "suc_")
        for spec in STAFF_PER_TENANT:
            id_staff = f"{tenant}_{spec['id_staff_suffix']}"
            email = f"{spec['email_suffix']}@{tenant}.papasqueens.test"
            item = {
                "tenant_id": tenant,
                "id_staff": id_staff,
                "name": spec["name"],
                "dni": spec["dni"],
                "role": spec["role"],
                "email": email,
                "password_hash": password_h,
                "status": spec["status"],
                "phone": spec["phone"],
                "hire_date": now,
                "id_sucursal": id_sucursal,
            }
            print(f"Seeding staff: {item['tenant_id']} / {item['id_staff']} ({item['email']})")
            table.put_item(Item=item)

    print("Seed de Staff completado. Password por defecto:", default_password)


if __name__ == "__main__":
    main()