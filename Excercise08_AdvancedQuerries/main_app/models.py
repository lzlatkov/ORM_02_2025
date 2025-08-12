from decimal import Decimal
from django.core.validators import MinLengthValidator, MinValueValidator, EmailValidator, URLValidator
from django.db import models
from main_app.validators import validate_name, phone_validator
from main_app.mixins import RechargeEnergyMixin
# Create your models here.


class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[validate_name]
    )
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18, 'Age must be greater than or equal to 18')]
    )
    email = models.EmailField(
        error_messages={'invalid': "Enter a valid email address"}
    )
    phone_number = models.CharField(
        max_length=13,
        validators=[phone_validator]
    )
    website_url = models.URLField(
        error_messages={"invalid": "Enter a valid URL"}
    )


class BaseMedia(models.Model):
    title = models.CharField(
        max_length=100,
    )
    description = models.TextField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']


class Book(BaseMedia):
    author = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(5, 'Author must be at least 5 characters long')])
    isbn = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(6, 'ISBN must be at least 6 characters long')]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Book'
        verbose_name_plural = 'Models of type - Book'


class Movie(BaseMedia):
    director = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(8, 'Director must be at least 8 characters long')]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Movie'
        verbose_name_plural = 'Models of type - Movie'


class Music(BaseMedia):
    artist = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(9, 'Artist must be at least 9 characters long')]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Music'
        verbose_name_plural = 'Models of type - Music'


class Product(models.Model):
    TAX_PERCENT: Decimal = Decimal('0.08')
    SHIPPING_MULTIPLIER: Decimal = Decimal('2.00')

    name = models.CharField(
        max_length=100,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def calculate_tax(self) -> Decimal:
        return self.price * self.TAX_PERCENT

    def calculate_shipping_cost(self, weight: Decimal) -> Decimal:
        return weight * self.SHIPPING_MULTIPLIER

    def format_product_name(self) -> str:
        return f"Product: {self.name}"


class DiscountedProduct(Product):
    PRICE_INCREASE_PERCENT: Decimal = Decimal('0.20')
    TAX_PERCENT: Decimal = Decimal('0.05')
    SHIPPING_MULTIPLIER: Decimal = Decimal('1.50')

    class Meta:
        proxy = True

    def calculate_price_without_discount(self) -> Decimal:
        return Decimal(str(self.price)) * (1 + self.PRICE_INCREASE_PERCENT)

    def format_product_name(self) -> str:
        return f"Discounted Product: {self.name}"


class Hero(models.Model, RechargeEnergyMixin):
    ABILITY_ENERGY_REQUIRED: int = 0
    MIN_ENERGY: int = 1

    name = models.CharField(
        max_length=100,
    )
    hero_title = models.CharField(
        max_length=100,
    )
    energy = models.PositiveIntegerField()

    @property
    def required_energy_message(self) -> str:
        return ""

    @property
    def successful_ability_use_message(self) -> str:
        return ""

    def use_ability(self):
        if self.energy < self.ABILITY_ENERGY_REQUIRED:
            return self.required_energy_message

        if self.energy - self.ABILITY_ENERGY_REQUIRED > 0:
            self.energy -= self.ABILITY_ENERGY_REQUIRED
        else:
            self.energy = self.MIN_ENERGY

        self.save()

        return self.successful_ability_use_message


class SpiderHero(Hero):
    ABILITY_ENERGY_REQUIRED: int = 80

    class Meta:
        proxy = True

    @property
    def required_energy_message(self) -> str:
        return f"{self.name} as Spider Hero is out of web shooter fluid"

    @property
    def successful_ability_use_message(self) -> str:
        return f"{self.name} as Spider Hero swings from buildings using web shooters"

    def swing_from_buildings(self) -> str:
        return self.use_ability()


class FlashHero(Hero):
    ABILITY_ENERGY_REQUIRED: int = 65

    class Meta:
        proxy = True

    @property
    def required_energy_message(self) -> str:
        return f"{self.name} as Flash Hero needs to recharge the speed force"

    @property
    def successful_ability_use_message(self) -> str:
        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

    def run_at_super_speed(self) -> str:
        return self.use_ability()
