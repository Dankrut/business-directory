import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.models.building import BuildingOrm
from src.models.organization import OrganizationOrm
from src.models.phone import PhoneOrm
from src.models.activity import ActivityOrm
from src.config import settings

sync_url = settings.DB_URL.replace("+asyncpg", "")
engine = create_engine(sync_url)
Session = sessionmaker(bind=engine)


def clear_tables(session):
    """Очищаем все таблицы перед заполнением"""
    print("Очистка таблиц")
    session.execute(text("TRUNCATE TABLE phones RESTART IDENTITY CASCADE;"))
    session.execute(
        text("TRUNCATE TABLE organization_activities RESTART IDENTITY CASCADE;")
    )
    session.execute(text("TRUNCATE TABLE organizations RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE activities RESTART IDENTITY CASCADE;"))
    session.execute(text("TRUNCATE TABLE buildings RESTART IDENTITY CASCADE;"))
    session.commit()
    print("Таблицы очищены")


def seed():
    session = Session()
    try:
        # Очищаем таблицы
        clear_tables(session)

        # 1. Buildings
        print("Создание зданий")
        building1 = BuildingOrm(
            address="г. Москва, ул. Ленина 1", latitude=55.7558, longitude=37.6176
        )
        building2 = BuildingOrm(
            address="г. Москва, ул. Блюхера 32/1", latitude=55.7510, longitude=37.6200
        )
        building3 = BuildingOrm(
            address="г. Москва, ул. Тверская 15", latitude=55.7658, longitude=37.6076
        )

        session.add_all([building1, building2, building3])
        session.commit()
        print(f"Создано {session.query(BuildingOrm).count()} зданий")

        # 2. Activities
        print("Создание видов деятельности")
        food = ActivityOrm(name="Еда", level=1)
        cars = ActivityOrm(name="Автомобили", level=1)

        session.add_all([food, cars])
        session.commit()
        print("  - Созданы корневые категории")

        meat = ActivityOrm(name="Мясная продукция", parent_id=food.id, level=2)
        milk = ActivityOrm(name="Молочная продукция", parent_id=food.id, level=2)
        passenger = ActivityOrm(name="Легковые", parent_id=cars.id, level=2)
        trucks = ActivityOrm(name="Грузовые", parent_id=cars.id, level=2)

        session.add_all([meat, milk, passenger, trucks])
        session.commit()
        print("  - Созданы дочерние категории")

        parts = ActivityOrm(name="Запчасти", parent_id=passenger.id, level=3)
        accessories = ActivityOrm(name="Аксессуары", parent_id=passenger.id, level=3)

        session.add_all([parts, accessories])
        session.commit()
        print(f"Всего создано {session.query(ActivityOrm).count()} видов деятельности")

        # 3. Organizations
        print("Создание организаций")
        orgs = [
            OrganizationOrm(name="ООО Рога и Копыта", building_id=building1.id),
            OrganizationOrm(name="АвтоМир", building_id=building2.id),
            OrganizationOrm(name="Мясной Двор", building_id=building1.id),
            OrganizationOrm(name="Молочная Сказка", building_id=building3.id),
            OrganizationOrm(name="Автозапчасти 24/7", building_id=building2.id),
            OrganizationOrm(name="Грузоперевозки", building_id=building3.id),
        ]

        session.add_all(orgs)
        session.commit()
        print(f"Создано {len(orgs)} организаций")

        # 4. Связываем с деятельностью
        print("Связывание с деятельностью")
        orgs[0].activities = [meat, milk, food]  # Рога и Копыта
        orgs[1].activities = [passenger, parts, accessories]  # АвтоМир
        orgs[2].activities = [meat, food]  # Мясной Двор
        orgs[3].activities = [milk, food]  # Молочная Сказка
        orgs[4].activities = [parts, accessories]  # Автозапчасти
        orgs[5].activities = [trucks, cars]  # Грузоперевозки

        session.commit()

        # 5. Phones
        print("Создание телефонов")
        phones = [
            PhoneOrm(phone="2-222-222", organization_id=orgs[0].id),
            PhoneOrm(phone="3-333-333", organization_id=orgs[0].id),
            PhoneOrm(phone="8-923-666-13-13", organization_id=orgs[1].id),
            PhoneOrm(phone="+7 (495) 123-45-67", organization_id=orgs[1].id),
            PhoneOrm(phone="8-800-555-35-35", organization_id=orgs[2].id),
            PhoneOrm(phone="+7 (916) 234-56-78", organization_id=orgs[3].id),
            PhoneOrm(phone="+7 (985) 345-67-89", organization_id=orgs[4].id),
            PhoneOrm(phone="+7 (903) 456-78-90", organization_id=orgs[5].id),
            PhoneOrm(phone="8-495-765-43-21", organization_id=orgs[5].id),
        ]

        session.add_all(phones)
        session.commit()
        print(f"Создано {len(phones)} телефонов")

    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    seed()
