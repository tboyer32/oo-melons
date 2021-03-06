"""Classes for melon orders."""
import random
from datetime import datetime


class TooManyMelonsError(ValueError):

    def __init__(self):
        super().__init__("No more than 100 melons!")


class AbstractMelonOrder:

    def __init__(self, species, qty, order_type, tax):

        self.species = species
        self.order_type = order_type
        self.qty = qty 
        self.tax = tax
        self.shipped = False

        if self.qty > 100:
            raise TooManyMelonsError()

    def get_base_price(self):

        base_price = random.randrange(5,10)
        current_time = datetime.now()

        #check for rush hour
        if (current_time.hour >= 8 and current_time.hour <= 11) and (current_time.weekday < 5):

            base_price += 4

        return base_price

    def get_total(self):
        """Calculate price, including tax."""
        
        base_price = self.get_base_price()

        if self.species == "Christmas melon":
            base_price = base_price * 1.5

        total = (1 + self.tax) * self.qty * base_price

        if self.order_type == "international" and self.qty < 10:
            total += 3

        return total

    def mark_shipped(self):
        """Record the fact than an order has been shipped."""

        self.shipped = True


class DomesticMelonOrder(AbstractMelonOrder):
    """A melon order within the USA."""

    def __init__(self,species,qty):
        super().__init__(species, qty, "domestic", 0.08)


class InternationalMelonOrder(AbstractMelonOrder):
    """An international (non-US) melon order."""

    order_type = "international"
    tax = 0.17

    def __init__(self, species, qty, country_code):
        super().__init__(species, qty, "international", 0.17)
        """Initialize melon order attributes."""

        self.country_code = country_code

    def get_country_code(self):
        """Return the country code."""

        return self.country_code


class GovernmentMelonOrder(AbstractMelonOrder):

    def __init__(self,species,qty,passed_inspection=False):
        super().__init__(species, qty, "government", 0.00)

        self.passed_inspection = passed_inspection
        
    def mark_inspection(self, passed):
        if self.passed_inspection == True:
            self.passed_inspection = passed

            