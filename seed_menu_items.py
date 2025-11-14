import uuid
import os
from decimal import Decimal
import boto3

# Configuración
DYNAMO_REGION = "us-east-1"
TABLE_NAME = "MenuItems"
S3_BUCKET_NAME = "papasqueens-menu-images"
IMAGES_LOCAL_DIR = os.path.join(os.path.dirname(__file__), "menu-images")

TENANTS = [
    "tenant_pq_barranco",
    "tenant_pq_san_isidro",
    "tenant_pq_miraflores",
]

# Menú base de PapasQueen's
BASE_PRODUCTS = [
    # ALITAS
    {
        "nombre": "Alitas X 6 und",
        "descripcion": "6 alitas jugosas con 3 cremas a elección, 1 papa pequeña gratis y 1 salsa gratis.",
        "precio": 24.90,
        "precio_original": 33.50,
        "descuento_porcentaje": 26,
        "categoria": "ALITAS",
        "image_key": "alitas-x-6-und.jpg",
    },
    {
        "nombre": "Alitas X 8 und",
        "descripcion": "8 alitas jugosas con 3 cremas a elección, 1 papa pequeña gratis y 2 salsas gratis.",
        "precio": 31.90,
        "precio_original": 43.90,
        "descuento_porcentaje": 27,
        "categoria": "ALITAS",
        "image_key": "alitas-x-8-und.jpg",
    },
    {
        "nombre": "Alitas X 10 und",
        "descripcion": "10 alitas jugosas con 3 cremas a elección, 1 papa pequeña gratis y 2 salsas gratis.",
        "precio": 36.90,
        "precio_original": 49.90,
        "descuento_porcentaje": 26,
        "categoria": "ALITAS",
        "image_key": "alitas-x-10-und.jpg",
    },
    {
        "nombre": "Alitas X 16 und",
        "descripcion": "16 alitas jugosas con 5 cremas a elección, 2 papas pequeñas gratis y 3 salsas gratis.",
        "precio": 59.90,
        "precio_original": 81.90,
        "descuento_porcentaje": 27,
        "categoria": "ALITAS",
        "image_key": "alitas-x-16-und.jpg",
    },
    {
        "nombre": "Alitas X 20 und",
        "descripcion": "20 alitas jugosas con 5 cremas a elección, 2 papas pequeñas gratis y 4 salsas gratis.",
        "precio": 62.90,
        "precio_original": 94.90,
        "descuento_porcentaje": 34,
        "categoria": "ALITAS",
        "image_key": "alitas-x-20-und.jpg",
    },
    {
        "nombre": "Alitas X 24 und",
        "descripcion": "24 alitas jugosas con 6 cremas a elección, 3 papas pequeñas gratis y 4 salsas gratis.",
        "precio": 75.90,
        "precio_original": 102.90,
        "descuento_porcentaje": 26,
        "categoria": "ALITAS",
        "image_key": "alitas-x-24-und.jpg",
    },
    {
        "nombre": "Alitas X 30 und",
        "descripcion": "30 alitas jugosas con 7 cremas a elección, 4 papas pequeñas gratis y 6 salsas gratis.",
        "precio": 99.90,
        "precio_original": 134.90,
        "descuento_porcentaje": 26,
        "categoria": "ALITAS",
        "image_key": "alitas-x-30-und.jpg",
    },
    {
        "nombre": "Alitas X 40 und",
        "descripcion": "40 alitas jugosas con 10 cremas a elección, 1 papa familiar gratis y 6 salsas gratis.",
        "precio": 124.90,
        "precio_original": 168.90,
        "descuento_porcentaje": 26,
        "categoria": "ALITAS",
        "image_key": "alitas-x-40-und.jpg",
    },
    {
        "nombre": "Alitas X 50 und",
        "descripcion": "50 alitas jugosas con 14 cremas a elección, 1 papa familiar gratis y 7 salsas gratis.",
        "precio": 155.90,
        "precio_original": 210.90,
        "descuento_porcentaje": 26,
        "categoria": "ALITAS",
        "image_key": "alitas-x-50-und.jpg",
    },
    {
        "nombre": "Alitas X 100 und",
        "descripcion": "100 alitas jugosas con 30 cremas a elección, 2 papas familiares gratis y 7 salsas gratis.",
        "precio": 299.90,
        "precio_original": 404.90,
        "descuento_porcentaje": 26,
        "categoria": "ALITAS",
        "image_key": "alitas-x-100-und.jpg",
    },

    # COMBOS
    {
        "nombre": "Combo Express para 1 persona",
        "descripcion": "8 alitas, 2 salsas a elección, papas artesanales con cremas a elección y gaseosa de 500 ml.",
        "precio": 34.40,
        "precio_original": 46.90,
        "descuento_porcentaje": 27,
        "categoria": "COMBOS",
        "image_key": "combo-express-1-persona.jpg",
    },
    {
        "nombre": "Combo causitas para 4 personas",
        "descripcion": "30 alitas con 6 salsas a elección, papas crocantes artesanales tamaño familiar, 10 cremas y 4 Inca Kolas de 500 ml.",
        "precio": 109.90,
        "precio_original": 149.90,
        "descuento_porcentaje": 27,
        "categoria": "COMBOS",
        "image_key": "combo-causitas-4-personas.jpg",
    },
    {
        "nombre": "Dúo perfecto para 2 personas",
        "descripcion": "16 alitas fritas con 3 salsas a elección, papas fritas artesanales con cremas y 2 gaseosas de 500 ml.",
        "precio": 64.90,
        "precio_original": 88.90,
        "descuento_porcentaje": 27,
        "categoria": "COMBOS",
        "image_key": "duo-perfecto-2-personas.jpg",
    },

    # HAMBURGUESAS
    {
        "nombre": "Burger Bacon",
        "descripcion": "Hamburguesa de carne de res 120g a la plancha, tocino laminado, queso cheddar, lechuga, tomate y mayonesa, en pan suave.",
        "precio": 23.90,
        "precio_original": 23.90,
        "descuento_porcentaje": 0,
        "categoria": "HAMBURGUESAS",
        "image_key": "burger-bacon.jpg",
    },
    {
        "nombre": "Burger Chesse",
        "descripcion": "Hamburguesa de carne de res 120g a la plancha, queso cheddar derretido, lechuga, tomate y mayonesa, en pan suave.",
        "precio": 21.90,
        "precio_original": 21.90,
        "descuento_porcentaje": 0,
        "categoria": "HAMBURGUESAS",
        "image_key": "burger-chesse.jpg",
    },
    {
        "nombre": "Burger Clasica",
        "descripcion": "Hamburguesa de carne de res 120g a la plancha, con lechuga, tomate y mayonesa, en pan suave.",
        "precio": 16.90,
        "precio_original": 16.90,
        "descuento_porcentaje": 0,
        "categoria": "HAMBURGUESAS",
        "image_key": "burger-clasica.jpg",
    },
    {
        "nombre": "Burger Royal",
        "descripcion": "Hamburguesa de carne de res 120g, jamón tipo americano, queso cheddar, huevo, lechuga, tomate y mayonesa, en pan suave.",
        "precio": 24.90,
        "precio_original": 24.90,
        "descuento_porcentaje": 0,
        "categoria": "HAMBURGUESAS",
        "image_key": "burger-royal.jpg",
    },
    {
        "nombre": "Pq-broster Clasica",
        "descripcion": "Hamburguesa con pollo broaster crujiente de 90g, lechuga, tomate y mayonesa, en pan suave.",
        "precio": 14.90,
        "precio_original": 14.90,
        "descuento_porcentaje": 0,
        "categoria": "HAMBURGUESAS",
        "image_key": "pq-broster-clasica.jpg",
    },
    {
        "nombre": "Pq-broster Queso Tocino",
        "descripcion": "Hamburguesa con pollo broaster 90g, queso Edam derretido, tocino, lechuga, tomate y mayonesa, en pan suave.",
        "precio": 18.90,
        "precio_original": 18.90,
        "descuento_porcentaje": 0,
        "categoria": "HAMBURGUESAS",
        "image_key": "pq-broster-queso-tocino.jpg",
    },

    # SALCHIPAPAS
    {
        "nombre": "SalchiQueen's Especial Premium",
        "descripcion": "Papas fritas artesanales con hot dog y chorizo, cremas a elección y bebida de 500 ml (Coca Cola, Inka Kola, Chicha o Maracuyá).",
        "precio": 27.90,
        "precio_original": 27.90,
        "descuento_porcentaje": 0,
        "categoria": "SALCHIPAPAS",
        "image_key": "salchiqueens-especial-premium.jpg",
    },
    {
        "nombre": "SalchiQueen's Premium",
        "descripcion": "Papas fritas artesanales con hot dog, cremas a elección y bebida de 500 ml (Coca Cola, Inka Kola, Chicha o Maracuyá).",
        "precio": 24.90,
        "precio_original": 24.90,
        "descuento_porcentaje": 0,
        "categoria": "SALCHIPAPAS",
        "image_key": "salchiqueens-premium.jpg",
    },
    {
        "nombre": "Salchipollo Premium",
        "descripcion": "Pollo Broaster, cremas a elección y bebida de 500 ml (Coca Cola, Inka Kola, Chicha o Maracuyá).",
        "precio": 26.90,
        "precio_original": 26.90,
        "descuento_porcentaje": 0,
        "categoria": "SALCHIPAPAS",
        "image_key": "salchipollo-premium.jpg",
    },
]


def build_items_for_tenant(tenant_id: str):
    items = []
    for base in BASE_PRODUCTS:
        item = {
            "id_producto": str(uuid.uuid4()),
            "tenant_id": tenant_id,
            "nombre": base["nombre"],
            "descripcion": base["descripcion"],
            "precio": Decimal(str(base["precio"])),
            "precio_original": Decimal(str(base["precio_original"])),
            "descuento_porcentaje": Decimal(str(base["descuento_porcentaje"])),
            "categoria": base["categoria"],
            "image_key": base.get("image_key"),
            "image_url": f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{base['image_key']}" if base.get("image_key") else None,
            "available": True,
        }
        items.append(item)
    return items


def upload_images_to_s3(s3_client):
    uploaded = 0
    for base in BASE_PRODUCTS:
        image_key = base.get("image_key")
        if not image_key:
            continue

        local_path = os.path.join(IMAGES_LOCAL_DIR, image_key)
        if not os.path.isfile(local_path):
            print(f"[WARN] Imagen local no encontrada para {base['nombre']}: {local_path}")
            continue

        try:
            s3_client.upload_file(local_path, S3_BUCKET_NAME, image_key)
            uploaded += 1
        except Exception as e:
            print(f"[ERROR] No se pudo subir {image_key} a S3: {e}")

    print(f"seed imagenes: {uploaded} imágenes subidas a s3://{S3_BUCKET_NAME}/ desde {IMAGES_LOCAL_DIR}")


def seed():
    dynamo = boto3.resource("dynamodb", region_name=DYNAMO_REGION)
    table = dynamo.Table(TABLE_NAME)
    s3_client = boto3.client("s3", region_name=DYNAMO_REGION)

    all_items = []
    for tenant in TENANTS:
        all_items.extend(build_items_for_tenant(tenant))

    upload_images_to_s3(s3_client)

    with table.batch_writer() as batch:
        for item in all_items:
            batch.put_item(Item=item)

    print(f"seed completo: {len(all_items)} items insertados en {TABLE_NAME} para {len(TENANTS)} tenants.")


if __name__ == "__main__":
    seed()