import os
import uuid
import datetime

import bcrypt
import boto3

DYNAMO_REGION = "us-east-1"
TABLE_NAME = "Staff"

TENANTS = [
    "tenant_pq_barranco",
    "tenant_pq_san_isidro",
    "tenant_pq_miraflores",
]

STAFF_PER_TENANT = [
    {
        "id_staff_suffix": "admin",
        "name": "Administrador General",
        "dni": "00000000",
        "role": "admin",
        "email_suffix": "admin",
        "phone": "+51 900000001",
        "status": "activo",
    },
    {
        "id_staff_suffix": "kitchen1",
        "name": "Staff Cocina 1",
        "dni": "00000001",
        "role": "staff",
        "email_suffix": "cocina1",
        "phone": "+51 900000002",
        "status": "activo",
    },
    {
        "id_staff_suffix": "delivery1",
        "name": "Repartidor 1",
        "dni": "00000002",
        "role": "delivery",
        "email_suffix": "delivery1",
        "phone": "+51 900000003",
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