from collections import defaultdict
from typing import Iterable

from parcours_imi.models import AttributeConstraint


class AttributeConstraintsValidator:

    def __init__(self, constraints: Iterable[AttributeConstraint], attributes_getter):
        self.constraints = constraints
        self.attributes_getter = attributes_getter

    def validate(self, items):
        constraints_values = self._sum_constraints_values(items)

        validation_data = []
        for constraint in self.constraints:
            constraint_value = constraints_values[constraint.attribute]
            is_valid = True

            validation_message = f'{constraint.description} (valeur actuelle: {constraint_value})'

            if constraint.min_value is not None and constraint_value < constraint.min_value:
                is_valid = False

            if constraint.max_value is not None and constraint_value > constraint.max_value:
                is_valid = False

            validation_data.append(dict(
                message=validation_message,
                is_valid=is_valid,
            ))

        return validation_data

    def _sum_constraints_values(self, items):
        constraints_values = defaultdict(float)

        for item in items:
            attributes = self.attributes_getter(item)

            for attribute, value in attributes.items():
                constraints_values[attribute] += float(value)

        return constraints_values
