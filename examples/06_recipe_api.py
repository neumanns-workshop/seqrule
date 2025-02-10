"""
This example demonstrates how to use the seqrule API to validate cooking
recipes, enforcing rules like:
- Ingredient sequencing (e.g., yeast before flour)
- Temperature constraints (e.g., refrigeration after dairy)
- Time constraints (e.g., minimum resting times)
- Equipment dependencies (e.g., mixer before dough hook)
- Food safety rules (e.g., minimum cooking temperatures)
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional

import aiohttp

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

# API configuration
API_URL = "http://localhost:8000"


async def create_recipe_step(
    name: str,
    ingredients: List[str],
    equipment: List[str],
    temperature: Optional[float] = None,
    duration_minutes: Optional[int] = None,
    requires_refrigeration: bool = False
) -> Dict:
    """Create a recipe step object for API validation."""
    return {
        "name": name,
        "properties": {
            "ingredients": ", ".join(ingredients) if ingredients else "",
            "equipment": equipment[0] if equipment else "",
            "temperature": (
                float(temperature) if temperature is not None else None
            ),
            "duration_minutes": (
                int(duration_minutes) if duration_minutes is not None
                else None
            ),
            "requires_refrigeration": bool(requires_refrigeration)
        }
    }


def check_temperature_sequence(obj, context):
    """Check if temperature changes are safe and logical."""
    prev = context['prev']
    if not prev:
        return True

    curr_temp = obj.get('temperature')
    prev_temp = prev.get('temperature')

    # Skip if temperatures not specified
    if curr_temp is None or prev_temp is None:
        return True

    # Temperature changes should be gradual (no more than 50°C difference)
    if abs(curr_temp - prev_temp) > 50:
        print(
            "Temperature change too drastic: "
            f"{prev_temp}°C -> {curr_temp}°C"
        )
        return False

    return True


def check_equipment_dependency(obj, context):
    """Check if required equipment is used in the correct order."""
    equipment = obj.get('equipment', [])

    # Define equipment dependencies
    dependencies = {
        'dough_hook': ['mixer'],  # Dough hook requires mixer first
        'food_processor': ['cutting_board'],  # Processing requires prep
        'oven': ['baking_sheet', 'baking_pan']  # Oven requires baking vessel
    }

    # Check each piece of equipment
    for item in equipment:
        if item in dependencies:
            # Get all previous equipment used
            prev_equipment = set()
            idx = context['index']
            sequence = context['sequence']
            for i in range(idx):
                prev_equipment.update(sequence[i].get('equipment', []))

            # Check if required equipment was used
            required = dependencies[item]
            if not any(req in prev_equipment for req in required):
                print(f"{item} requires one of {required} to be used first")
                return False

    return True


async def create_recipe_rule(session) -> Dict:
    """Create a recipe validation rule via API."""
    rule_request = {
        "conditions": [
            # Temperature safety rules
            {
                "property_name": "temperature",
                "operator": "<=",
                "value": 200  # Maximum allowed temperature
            },
            {
                "property_name": "temperature",
                "operator": ">=",
                "value": 0  # Minimum allowed temperature
            },
            # Duration constraints
            {
                "property_name": "duration_minutes",
                "operator": ">",
                "value": 0  # All steps must take some time
            }
        ],
        "sequence": ["mix", "rest", "shape", "bake"]
    }

    async with session.post(f"{API_URL}/rules", json=rule_request) as response:
        return await response.json()


async def evaluate_recipe(session, recipe_steps: List[Dict]) -> Dict:
    """Evaluate a recipe sequence via API."""
    evaluate_request = {
        "objects": recipe_steps
    }

    rule_request = {
        "conditions": [
            # Temperature safety rules
            {
                "property_name": "temperature",
                "operator": "<=",
                "value": 200  # Maximum allowed temperature
            },
            {
                "property_name": "temperature",
                "operator": ">=",
                "value": 0  # Minimum allowed temperature
            },
            # Duration constraints
            {
                "property_name": "duration_minutes",
                "operator": ">",
                "value": 0  # All steps must take some time
            }
        ],
        "sequence": ["mix", "rest", "shape", "bake"]
    }

    async with session.post(
        f"{API_URL}/rules/evaluate",
        json={
            "evaluate_request": evaluate_request,
            "rule_request": rule_request
        }
    ) as response:
        return await response.json()


async def analyze_rule_complexity(session) -> Dict:
    """Analyze rule complexity via API."""
    request = {
        "conditions": [
            # Temperature safety rules
            {
                "property_name": "temperature",
                "operator": "<=",
                "value": 200
            },
            {
                "property_name": "temperature",
                "operator": ">=",
                "value": 0
            },
            # Duration constraints
            {
                "property_name": "duration_minutes",
                "operator": ">",
                "value": 0
            }
        ],
        "sequence": ["mix", "rest", "shape", "bake"]
    }

    async with session.post(
        f"{API_URL}/rules/analyze",
        json=request
    ) as response:
        return await response.json()


async def main():
    """Example usage of recipe validation via API."""
    print("Recipe Validation API Example")
    print("============================\n")

    # Create recipe steps for bread making
    bread_recipe = [
        await create_recipe_step(
            name="mix",
            ingredients=["flour", "yeast", "water", "salt"],
            equipment=["mixer"],
            temperature=25.0,
            duration_minutes=10
        ),
        await create_recipe_step(
            name="rest",
            ingredients=[],
            equipment=["bowl"],
            temperature=22.0,
            duration_minutes=60,
            requires_refrigeration=False
        ),
        await create_recipe_step(
            name="shape",
            ingredients=[],
            equipment=["board"],
            temperature=22.0,
            duration_minutes=15
        ),
        await create_recipe_step(
            name="bake",
            ingredients=[],
            equipment=["oven"],
            temperature=180.0,
            duration_minutes=30
        )
    ]

    # Invalid recipe with multiple rule violations
    invalid_recipe = [
        await create_recipe_step(
            name="mix",
            ingredients=["flour", "water"],  # Missing yeast
            equipment=["spoon"],  # Wrong equipment
            temperature=-5.0,  # Too cold
            duration_minutes=0  # Invalid duration
        ),
        await create_recipe_step(
            name="rest",
            ingredients=[],
            equipment=["counter"],
            temperature=30.0,  # Too warm for resting
            duration_minutes=10  # Too short rest
        ),
        await create_recipe_step(
            name="shape",
            ingredients=["flour"],  # Shouldn't need more flour
            equipment=["hands"],
            temperature=25.0,
            duration_minutes=5  # Too short
        ),
        await create_recipe_step(
            name="bake",
            ingredients=[],
            equipment=["stovetop"],  # Wrong equipment
            temperature=220.0,  # Too hot
            duration_minutes=15  # Too short
        )
    ]

    async with aiohttp.ClientSession() as session:
        # Create the rule
        print("Creating recipe validation rule...")
        rule_response = await create_recipe_rule(session)
        print(f"Rule created: {json.dumps(rule_response, indent=2)}\n")

        # Test valid recipe
        print("Testing valid bread recipe...")
        valid_result = await evaluate_recipe(session, bread_recipe)
        print(f"Valid recipe result: {json.dumps(valid_result, indent=2)}\n")

        # Test invalid recipe
        print("Testing invalid recipe...")
        invalid_result = await evaluate_recipe(session, invalid_recipe)
        print(
            "Invalid recipe result: "
            f"{json.dumps(invalid_result, indent=2)}\n"
        )

        # Analyze rule complexity
        print("Analyzing rule complexity...")
        complexity = await analyze_rule_complexity(session)
        print(f"Complexity analysis: {json.dumps(complexity, indent=2)}")


if __name__ == "__main__":
    asyncio.run(main())
