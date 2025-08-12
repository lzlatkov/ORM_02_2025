import os
from decimal import Decimal

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character
# Create queries within functions

###############################3


def create_pet(name: str, species: str):
    pet = Pet.objects.create(name=name, species=species)
    return f"{pet.name} is a very cute {pet.species}!"
    #pet = Pet(name=name, species=species)
    #pet.save()

##########################################


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    artifact = Artifact.objects.create(name=name, origin=origin, age=age, description=description, is_magical=is_magical)
    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.age > 250 and artifact.is_magical:
        artifact.name = new_name
        artifact.save()
    #Artifact.objects.filter(is_magical=True, age__gt=250).update(name=new_name)

def delete_all_artifacts():
    artifacts = Artifact.objects.all()
    for artifact in artifacts:
        artifact.delete()

    #Artifacts.objects.all().delete()

#########################################


def show_all_locations():
    locations = Location.objects.all().order_by('-id')
    return '\n'.join(f"{l.name} has a population of {l.population}!" for l in locations)


def new_capital():
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()
################################################


def apply_discount():
    cars = Car.objects.all()
    for car in cars:
        car.discount_percent = Decimal(str((sum(int(digit) for digit in str(car.year))) / 100))
        car.price_with_discount = car.price - (car.price * car.discount_percent)
        car.save()


def get_recent_cars():
    return Car.objects.filter(year__gt=2020).values('model', 'price')


def delete_last_car():
    Car.objects.last().delete()

#################################


def show_unfinished_tasks():
    unfinished_tasks = Task.objects.filter(is_finished=False)
    return '\n'.join(f"Task - {t.title} needs to be done until {t.due_date}!" for t in unfinished_tasks)


def complete_odd_tasks():
    for task in Task.objects.all():
        if task.id % 2 == 1:
            task.is_finished = True
            task.save()


def encode_and_replace(text: str, task_title: str) -> None:

    encoded_text = ''.join(chr(ord(t) - 3) for t in text)

    for task in Task.objects.filter(title=task_title):
        task.description = encoded_text
        task.save()
#############################


def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type=HotelRoom.RoomTypes.Deluxe)
    return '\n'.join(f"Deluxe room with number {r.room_number} costs {r.price_per_night}$ per night!" for r in deluxe_rooms if r.id % 2 == 0)


def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by('id')
    previous_room: HotelRoom = None

    for room in rooms:
        if not room.is_reserved:
            continue
        if previous_room:
            room.capacity += previous_room.capacity
        else:
            room.capacity += room.id

        previous_room = room
        room.save()


def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()
    if not last_room.is_reserved:
        last_room.delete()
################################################


def update_characters():
    characters = Character.objects.all()
    for character in characters:
        if character.class_name == "Mage":
            character.level += 3
            character.intelligence -= 7
            character.save()
        elif character.class_name == "Warrior":
            character.hit_points //= 2
            character.dexterity += 4
            character.save()
        elif character.class_name == "Assassin" or character.class_name == "Scout":
            character.inventory = "The inventory is empty"
            character.save()


def fuse_characters(first_character: Character, second_character: Character):
    fusion_inventory = None

    if first_character.class_name in [Character.Classes.Mage, Character.Classes.Scout]:
        fusion_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    elif first_character.class_name in [Character.Classes.Warrior, Character.Classes.Assassin]:
        fusion_inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=first_character.name + ' ' + second_character.name,
        class_name=Character.Classes.Fusion,
        level=(first_character.level + second_character.level) // 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory=fusion_inventory
    )
    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.update(dexterity=30)
    # characters = Character.objects.all()
    # for character in characters:
    #     character.dexterity += 30
    #     character.save()


def grand_intelligence():
    Character.objects.update(intelligence=40)


def grand_strength():
    Character.objects.update(strength=50)


def delete_characters():
    characters = Character.objects.filter(inventory="The inventory is empty").delete()


