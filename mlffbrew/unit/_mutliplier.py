from typing import Dict
from dataclasses import dataclass


@dataclass
class UnitDictionaries:
    length: Dict[str, float] = None
    energy: Dict[str, float] = None
    header: Dict[str, str] = None
    special: Dict[str, str] = None

    def __post_init__(self):
        self.length = {"angstrom": 1.0, "nm": 10.0, "bohr": 0.529177210903, "m": 1e10}
        self.energy = {"J": 1.0, "eV": 1.602176634e-19, "hatree": 4.3597447222071e-18}
        self.header = {"G": "1e9*", "M": "1e6*"}
        self.special = {"Pa": "J/m^3", "N": "J/m"}


class UnitMultiplierCreator:
    def __init__(self, expression: str, *, sep: str = "->") -> None:
        """
        Initialize unit converter with an expression and separator.

        Args:
            expression: Unit conversion expression (e.g., "eV->J")
            sep: Separator between units (default: "->")
        """
        self._sep = sep
        self._expression = expression
        self._units = UnitDictionaries()
        self._multiplicity = self._evaluate_expression()

    def _evaluate_expression(self) -> float:
        """Evaluate the conversion expression and return the multiplicity factor."""
        processed_expr = self._process_expression()
        try:
            return eval(processed_expr)
        except Exception as e:
            raise ValueError(f"Invalid conversion expression: {self._expression}") from e

    def _process_expression(self) -> str:
        """Process the expression by replacing unit symbols with their values."""
        expr = f"({self._encode_special_cases()})"

        # Replace units with their values
        for unit_dict in [self._units.length, self._units.energy, self._units.header]:
            for unit, value in unit_dict.items():
                expr = expr.replace(unit, str(value))

        # Replace operators
        expr = expr.replace("^", "**")
        expr = expr.replace(self._sep, ")/(")
        return expr

    def _encode_special_cases(self) -> str:
        """Handle special unit cases like Pa and N."""
        result = self._expression
        for unit, replacement in self._units.special.items():
            result = result.replace(unit, replacement)
        return result

    def __repr__(self) -> str:
        return str(self._multiplicity)

    def __float__(self) -> float:
        return float(self._multiplicity)


# Convenience function
def create_multiplier(expression: str, sep: str = "->") -> float:
    """
    Create a UnitConverter instance.

    Args:
        expression: Unit conversion expression
        sep: Separator between units

    Returns:
        UnitConverter instance
    """
    return float(UnitMultiplierCreator(expression, sep=sep))
