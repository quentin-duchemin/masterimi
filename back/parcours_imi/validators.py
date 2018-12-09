from collections import defaultdict
from enum import Enum
from typing import Iterable

from intervaltree import IntervalTree


class ConstraintType(Enum):
    VALID = 'valid'
    WARNING = 'warning'
    ERROR = 'error'


def build_validation_entry(validation_message: str, constraint_type: ConstraintType):
        if constraint_type == ConstraintType.VALID:
            tag = 'OK'
        elif constraint_type == ConstraintType.WARNING:
            tag = 'ATTENTION'
        elif constraint_type == ConstraintType.ERROR:
            tag = 'ERREUR'
        else:
            raise NotImplementedError()

        return dict(
            message=validation_message,
            type=constraint_type.value,
            full_message=f"[{tag}] {validation_message}",
        )


class AttributeConstraintsValidator:

    def __init__(self, constraints: Iterable['AttributeConstraint'], attributes_getter):
        self.constraints = constraints
        self.attributes_getter = attributes_getter

    def validate(self, items):
        constraints_values = self._sum_constraints_values(items)

        validation_data = []
        for constraint in self.constraints:
            constraint_value = constraints_values[constraint.attribute]
            constraint_type = ConstraintType.VALID

            validation_message = f'{constraint.description} (valeur actuelle: {constraint_value})'

            if constraint.min_value is not None and constraint_value < constraint.min_value:
                constraint_type = ConstraintType.ERROR

            if constraint.max_value is not None and constraint_value > constraint.max_value:
                constraint_type = ConstraintType.ERROR

            validation_data.append(build_validation_entry(validation_message, constraint_type))

        return validation_data

    def _sum_constraints_values(self, items):
        constraints_values = defaultdict(float)

        for item in items:
            attributes = self.attributes_getter(item)

            for attribute, value in attributes.items():
                constraints_values[attribute] += float(value)

        return constraints_values


class TimeCollisionValidator:

    def validate(self, items):
        day_trees = defaultdict(IntervalTree)

        for item in items:
            time = item.time

            if not time:
                continue

            day, start, end = time.split('/')
            start = self.time_to_seconds(start)
            end = self.time_to_seconds(end)

            day_trees[f'{item.period}-{day}'][start:end] = item

        collisions = []
        for tree in day_trees.values():
            for boundary in tree.boundary_table:
                intervals = tree[boundary]

                if len(intervals) > 1:
                    collisions.append([
                        f'{interval.data.name} ({interval.data.period}-{interval.data.time})'
                        for interval in intervals
                    ])

        validation_data = []
        for collision in collisions:
            collided_courses = ' / '.join(collision)
            validation_message = f'Deux cours sur le même créneau : {collided_courses}'
            validation_data.append(build_validation_entry(validation_message, ConstraintType.WARNING))

        return validation_data

    def time_to_seconds(self, time: str):
        hours, minutes = time.split(':')
        return int(hours) * 60 + int(minutes)


def get_parcours_courses_rules_validation_data(parcours, main_courses, option_courses):
    attribute_constraints_validator = AttributeConstraintsValidator(
        constraints=parcours.master.attribute_constraints.all(),
        attributes_getter=lambda course: course.attributes,
    )
    attribute_constraints_validation_data = attribute_constraints_validator.validate(
        main_courses
    )

    time_collision_validation_data = TimeCollisionValidator().validate(
        main_courses + option_courses
    )

    if parcours.option == '3A-M2-ECTS':
        from parcours_imi.models import AttributeConstraint
        option_validator = AttributeConstraintsValidator(
            constraints=[
                AttributeConstraint.objects.get(pk='8ce0b5ea-7e1d-4d7a-b5e6-77c83ed0d4d9')
            ],
            attributes_getter=lambda course: dict(imi_ects_option2=course.ECTS),
        )
        option_validation_data = option_validator.validate(option_courses)

        return attribute_constraints_validation_data + option_validation_data + time_collision_validation_data

    return attribute_constraints_validation_data + time_collision_validation_data
