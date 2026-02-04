"""
MegaCalculator 3000 - A Comprehensive Scientific Calculator
Version 1.0.0
Over 1000 lines of advanced calculator functionality
"""

import math
import statistics
import cmath
import random
import datetime
import decimal
import fractions
import re
import json
import os
from typing import Union, List, Tuple, Dict, Any, Optional
from collections import defaultdict
from enum import Enum
from functools import wraps
import time
import sys
import traceback

# ==================== DECORATORS ====================
def timing_decorator(func):
    """Decorator to measure execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        return result, execution_time
    return wrapper

def error_handler(func):
    """Decorator to handle errors gracefully"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ZeroDivisionError:
            return "Error: Division by zero"
        except ValueError as e:
            return f"Error: {str(e)}"
        except OverflowError:
            return "Error: Numerical overflow"
        except Exception as e:
            return f"Error: {type(e).__name__}: {str(e)}"
    return wrapper

def validate_input(func):
    """Decorator to validate input parameters"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float, complex)):
                continue
            if isinstance(arg, str):
                try:
                    float(arg)
                except ValueError:
                    return "Error: Invalid input type"
        return func(*args, **kwargs)
    return wrapper

# ==================== ENUMS ====================
class CalculatorMode(Enum):
    BASIC = "basic"
    SCIENTIFIC = "scientific"
    PROGRAMMER = "programmer"
    STATISTICS = "statistics"
    GRAPHING = "graphing"
    FINANCIAL = "financial"
    MATRIX = "matrix"
    UNIT_CONVERSION = "unit_conversion"
    DATE_CALCULATION = "date_calculation"

class AngleMode(Enum):
    DEGREES = "degrees"
    RADIANS = "radians"
    GRADIANS = "gradians"

class NumberSystem(Enum):
    DECIMAL = 10
    BINARY = 2
    OCTAL = 8
    HEXADECIMAL = 16

# ==================== BASE CLASSES ====================
class HistoryEntry:
    """Class to represent a calculation history entry"""
    def __init__(self, expression: str, result: Any, timestamp: datetime.datetime = None):
        self.expression = expression
        self.result = result
        self.timestamp = timestamp or datetime.datetime.now()
        self.id = hash(f"{expression}{result}{self.timestamp}")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'expression': self.expression,
            'result': str(self.result),
            'timestamp': self.timestamp.isoformat(),
            'id': self.id
        }
    
    def __str__(self) -> str:
        return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.expression} = {self.result}"

class MemoryBank:
    """Class to handle calculator memory operations"""
    def __init__(self):
        self.memory = 0.0
        self.memory_slots = defaultdict(float)
        self.variables = {}
        self.constants = {
            'π': math.pi,
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau,
            'inf': float('inf'),
            'nan': float('nan'),
            'c': 299792458,  # Speed of light
            'G': 6.67430e-11,  # Gravitational constant
            'h': 6.62607015e-34,  # Planck's constant
            'g': 9.80665,  # Standard gravity
        }
    
    def store(self, value: float, slot: int = 0) -> None:
        """Store value in memory slot"""
        self.memory_slots[slot] = float(value)
    
    def recall(self, slot: int = 0) -> float:
        """Recall value from memory slot"""
        return self.memory_slots[slot]
    
    def clear_memory(self, slot: Optional[int] = None) -> None:
        """Clear memory slot or all memory"""
        if slot is None:
            self.memory_slots.clear()
            self.variables.clear()
        elif slot in self.memory_slots:
            del self.memory_slots[slot]
    
    def add_to_memory(self, value: float, slot: int = 0) -> None:
        """Add value to existing memory"""
        self.memory_slots[slot] += value
    
    def subtract_from_memory(self, value: float, slot: int = 0) -> None:
        """Subtract value from existing memory"""
        self.memory_slots[slot] -= value
    
    def define_variable(self, name: str, value: float) -> None:
        """Define a custom variable"""
        self.variables[name] = float(value)
    
    def get_variable(self, name: str) -> Optional[float]:
        """Get variable value"""
        return self.variables.get(name, self.constants.get(name))

# ==================== CALCULATOR ENGINE ====================
class MegaCalculator:
    """Main calculator class with 1000+ lines of functionality"""
    
    def __init__(self):
        self.history: List[HistoryEntry] = []
        self.memory_bank = MemoryBank()
        self.current_mode = CalculatorMode.SCIENTIFIC
        self.angle_mode = AngleMode.DEGREES
        self.number_system = NumberSystem.DECIMAL
        self.precision = 12
        self.is_radians = False
        self.is_gradians = False
        self.expression_buffer = ""
        self.result_buffer = ""
        self.last_result = 0.0
        self.settings = {
            'auto_parentheses': True,
            'thousands_separator': True,
            'sound_feedback': False,
            'theme': 'dark',
            'language': 'english',
            'decimal_places': 12,
            'angle_unit': 'degrees',
            'number_format': 'decimal',
            'save_history': True,
            'auto_power_off': 30,
        }
        self.initialize_functions()
        self.initialize_unit_conversions()
        self.initialize_financial_functions()
        self.initialize_matrix_operations()
        self.initialize_statistical_functions()
        
        # Statistics storage
        self.statistical_data = []
        self.regression_data = {'x': [], 'y': []}
        
        # Graph data storage
        self.graph_data = {'functions': [], 'points': [], 'ranges': {}}
    
    # ==================== INITIALIZATION METHODS ====================
    def initialize_functions(self) -> None:
        """Initialize mathematical function mappings"""
        self.functions = {
            # Basic arithmetic
            'add': lambda a, b: a + b,
            'subtract': lambda a, b: a - b,
            'multiply': lambda a, b: a * b,
            'divide': lambda a, b: a / b,
            'power': lambda a, b: a ** b,
            'root': lambda a, b: a ** (1/b),
            'mod': lambda a, b: a % b,
            'floor_div': lambda a, b: a // b,
            
            # Scientific functions
            'sin': self.sin,
            'cos': self.cos,
            'tan': self.tan,
            'asin': self.asin,
            'acos': self.acos,
            'atan': self.atan,
            'atan2': self.atan2,
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
            'asinh': math.asinh,
            'acosh': math.acosh,
            'atanh': math.atanh,
            
            'log': math.log10,
            'ln': math.log,
            'log2': math.log2,
            'exp': math.exp,
            'sqrt': math.sqrt,
            'cbrt': lambda x: x ** (1/3),
            'abs': abs,
            'factorial': math.factorial,
            'gamma': math.gamma,
            'lgamma': math.lgamma,
            'erf': math.erf,
            'erfc': math.erfc,
            
            # Statistical functions
            'mean': statistics.mean,
            'median': statistics.median,
            'mode': statistics.mode,
            'stdev': statistics.stdev,
            'variance': statistics.variance,
            'correlation': lambda x, y: statistics.correlation(x, y) if hasattr(statistics, 'correlation') else None,
            
            # Constants
            'pi': lambda: math.pi,
            'e': lambda: math.e,
            'tau': lambda: math.tau,
            'inf': lambda: float('inf'),
        }
    
    def initialize_unit_conversions(self) -> None:
        """Initialize unit conversion factors"""
        self.unit_conversions = {
            'length': {
                'meters': 1.0,
                'kilometers': 1000.0,
                'centimeters': 0.01,
                'millimeters': 0.001,
                'miles': 1609.344,
                'yards': 0.9144,
                'feet': 0.3048,
                'inches': 0.0254,
                'nautical_miles': 1852.0,
                'light_years': 9.461e15,
                'parsecs': 3.086e16,
            },
            'mass': {
                'kilograms': 1.0,
                'grams': 0.001,
                'pounds': 0.45359237,
                'ounces': 0.028349523125,
                'tons': 1000.0,
                'metric_tons': 1000.0,
                'carats': 0.0002,
            },
            'temperature': {
                'celsius': ('celsius', lambda x: x, lambda x: x),
                'fahrenheit': ('fahrenheit', lambda x: (x - 32) * 5/9, lambda x: x * 9/5 + 32),
                'kelvin': ('kelvin', lambda x: x - 273.15, lambda x: x + 273.15),
                'rankine': ('rankine', lambda x: (x - 491.67) * 5/9, lambda x: x * 9/5 + 491.67),
            },
            'time': {
                'seconds': 1.0,
                'milliseconds': 0.001,
                'microseconds': 1e-6,
                'nanoseconds': 1e-9,
                'minutes': 60.0,
                'hours': 3600.0,
                'days': 86400.0,
                'weeks': 604800.0,
                'years': 31536000.0,
                'leap_years': 31622400.0,
            },
            'area': {
                'square_meters': 1.0,
                'square_kilometers': 1e6,
                'square_centimeters': 1e-4,
                'square_millimeters': 1e-6,
                'square_miles': 2.589988e6,
                'acres': 4046.8564224,
                'hectares': 10000.0,
                'square_feet': 0.09290304,
                'square_inches': 0.00064516,
            },
            'volume': {
                'cubic_meters': 1.0,
                'liters': 0.001,
                'milliliters': 1e-6,
                'gallons': 0.003785411784,
                'quarts': 0.000946352946,
                'pints': 0.000473176473,
                'cups': 0.0002365882365,
                'fluid_ounces': 2.95735295625e-5,
                'cubic_feet': 0.028316846592,
                'cubic_inches': 1.6387064e-5,
            },
            'speed': {
                'meters_per_second': 1.0,
                'kilometers_per_hour': 0.2777777778,
                'miles_per_hour': 0.44704,
                'knots': 0.5144444444,
                'feet_per_second': 0.3048,
                'mach': 340.3,
                'light_speed': 299792458.0,
            },
            'pressure': {
                'pascals': 1.0,
                'kilopascals': 1000.0,
                'megapascals': 1e6,
                'bars': 100000.0,
                'millibars': 100.0,
                'atmospheres': 101325.0,
                'torr': 133.322368421,
                'psi': 6894.757293168,
            },
            'energy': {
                'joules': 1.0,
                'kilojoules': 1000.0,
                'calories': 4.184,
                'kilocalories': 4184.0,
                'kilowatt_hours': 3.6e6,
                'electronvolts': 1.602176634e-19,
                'btu': 1055.05585262,
                'therms': 1.055e8,
            },
            'power': {
                'watts': 1.0,
                'kilowatts': 1000.0,
                'megawatts': 1e6,
                'gigawatts': 1e9,
                'horsepower': 745.699871582,
                'metric_horsepower': 735.49875,
                'btu_per_hour': 0.2930710702,
            },
            'data': {
                'bits': 1.0,
                'bytes': 8.0,
                'kilobits': 1000.0,
                'kilobytes': 8000.0,
                'megabits': 1e6,
                'megabytes': 8e6,
                'gigabits': 1e9,
                'gigabytes': 8e9,
                'terabits': 1e12,
                'terabytes': 8e12,
                'petabits': 1e15,
                'petabytes': 8e15,
                'kibibits': 1024.0,
                'kibibytes': 8192.0,
                'mebibits': 1048576.0,
                'mebibytes': 8388608.0,
                'gibibits': 1073741824.0,
                'gibibytes': 8589934592.0,
            },
            'angle': {
                'degrees': 1.0,
                'radians': 57.29577951308232,
                'gradians': 0.9,
                'arcminutes': 1/60,
                'arcseconds': 1/3600,
                'turns': 360.0,
                'quadrants': 90.0,
                'sextants': 60.0,
            },
        }
    
    def initialize_financial_functions(self) -> None:
        """Initialize financial calculation functions"""
        self.financial_functions = {
            'fv': self.future_value,
            'pv': self.present_value,
            'npv': self.net_present_value,
            'irr': self.internal_rate_of_return,
            'pmt': self.payment,
            'nper': self.number_of_periods,
            'rate': self.interest_rate,
            'mirr': self.modified_internal_rate_of_return,
            'db': self.declining_balance_depreciation,
            'syd': self.sum_of_years_digits_depreciation,
            'sln': self.straight_line_depreciation,
            'ddb': self.double_declining_balance_depreciation,
        }
    
    def initialize_matrix_operations(self) -> None:
        """Initialize matrix operations"""
        self.matrix_operations = {
            'add': self.matrix_add,
            'subtract': self.matrix_subtract,
            'multiply': self.matrix_multiply,
            'transpose': self.matrix_transpose,
            'determinant': self.matrix_determinant,
            'inverse': self.matrix_inverse,
            'eigenvalues': self.matrix_eigenvalues,
            'eigenvectors': self.matrix_eigenvectors,
        }
    
    def initialize_statistical_functions(self) -> None:
        """Initialize advanced statistical functions"""
        self.statistical_functions = {
            'regression': self.linear_regression,
            'correlation_matrix': self.correlation_matrix,
            'histogram': self.create_histogram,
            'probability_distribution': self.probability_distribution,
            'confidence_interval': self.confidence_interval,
            'hypothesis_test': self.hypothesis_test,
            'anova': self.anova_test,
            'chi_square': self.chi_square_test,
        }
    
    # ==================== ANGLE CONVERSION METHODS ====================
    def to_radians(self, angle: float) -> float:
        """Convert angle to radians based on current angle mode"""
        if self.angle_mode == AngleMode.DEGREES:
            return math.radians(angle)
        elif self.angle_mode == AngleMode.GRADIANS:
            return angle * math.pi / 200
        else:  # RADIANS
            return angle
    
    def from_radians(self, radians: float) -> float:
        """Convert radians to current angle mode"""
        if self.angle_mode == AngleMode.DEGREES:
            return math.degrees(radians)
        elif self.angle_mode == AngleMode.GRADIANS:
            return radians * 200 / math.pi
        else:  # RADIANS
            return radians
    
    # ==================== TRIGONOMETRIC FUNCTIONS ====================
    @error_handler
    @validate_input
    def sin(self, angle: float) -> float:
        """Calculate sine with current angle mode"""
        return math.sin(self.to_radians(angle))
    
    @error_handler
    @validate_input
    def cos(self, angle: float) -> float:
        """Calculate cosine with current angle mode"""
        return math.cos(self.to_radians(angle))
    
    @error_handler
    @validate_input
    def tan(self, angle: float) -> float:
        """Calculate tangent with current angle mode"""
        return math.tan(self.to_radians(angle))
    
    @error_handler
    @validate_input
    def asin(self, value: float) -> float:
        """Calculate arcsine with current angle mode"""
        return self.from_radians(math.asin(value))
    
    @error_handler
    @validate_input
    def acos(self, value: float) -> float:
        """Calculate arccosine with current angle mode"""
        return self.from_radians(math.acos(value))
    
    @error_handler
    @validate_input
    def atan(self, value: float) -> float:
        """Calculate arctangent with current angle mode"""
        return self.from_radians(math.atan(value))
    
    @error_handler
    @validate_input
    def atan2(self, y: float, x: float) -> float:
        """Calculate arctangent of y/x with current angle mode"""
        return self.from_radians(math.atan2(y, x))
    
    # ==================== BASIC OPERATIONS ====================
    @error_handler
    @timing_decorator
    @validate_input
    def add(self, a: float, b: float) -> float:
        """Add two numbers"""
        result = a + b
        self._add_to_history(f"{a} + {b}", result)
        return result
    
    @error_handler
    @timing_decorator
    @validate_input
    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a"""
        result = a - b
        self._add_to_history(f"{a} - {b}", result)
        return result
    
    @error_handler
    @timing_decorator
    @validate_input
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers"""
        result = a * b
        self._add_to_history(f"{a} × {b}", result)
        return result
    
    @error_handler
    @timing_decorator
    @validate_input
    def divide(self, a: float, b: float) -> Union[float, str]:
        """Divide a by b"""
        if b == 0:
            return "Error: Division by zero"
        result = a / b
        self._add_to_history(f"{a} ÷ {b}", result)
        return result
    
    @error_handler
    @timing_decorator
    @validate_input
    def power(self, base: float, exponent: float) -> float:
        """Raise base to the power of exponent"""
        result = base ** exponent
        self._add_to_history(f"{base}^{exponent}", result)
        return result
    
    @error_handler
    @timing_decorator
    @validate_input
    def root(self, number: float, n: float) -> float:
        """Calculate nth root of number"""
        result = number ** (1/n)
        self._add_to_history(f"√[{n}]({number})", result)
        return result
    
    @error_handler
    @timing_decorator
    @validate_input
    def factorial(self, n: int) -> int:
        """Calculate factorial of n"""
        if n < 0:
            raise ValueError("Factorial of negative number is undefined")
        if n > 1000:
            raise ValueError("Number too large for factorial calculation")
        result = math.factorial(n)
        self._add_to_history(f"{n}!", result)
        return result
    
    @error_handler
    @timing_decorator
    @validate_input
    def modulo(self, a: float, b: float) -> float:
        """Calculate a modulo b"""
        result = a % b
        self._add_to_history(f"{a} mod {b}", result)
        return result
    
    @error_handler
    @timing_decorator
    @validate_input
    def percentage(self, value: float, percent: float) -> float:
        """Calculate percentage of value"""
        result = value * percent / 100
        self._add_to_history(f"{value} × {percent}%", result)
        return result
    
    # ==================== SCIENTIFIC FUNCTIONS ====================
    @error_handler
    @timing_decorator
    @validate_input
    def logarithm(self, number: float, base: float = 10.0) -> float:
        """Calculate logarithm of number with given base"""
        if number <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers")
        if base <= 0 or base == 1:
            raise ValueError("Invalid logarithm base")
        result = math.log(number, base)
        self._add_to_history(f"log_{base}({number})", result)
        return result
    
    @error_handler
    @timing_decorator
    @validate_input
    def natural_log(self, number: float) -> float:
        """Calculate natural logarithm of number"""
        if number <= 0:
            raise ValueError("Natural logarithm undefined for non-positive numbers")
        result = math.log(number)
        self._add_to_history(f"ln({number})", result)
        return result
    
    @error_handler
    @timing_decorator
    @validate_input
    def exponential(self, x: float) -> float:
        """Calculate e raised to the power of x"""
        result = math.exp(x)
        self._add_to_history(f"e^{x}", result)
        return result
    
    @error_handler
    @timing_decorator
    @validate_input
    def square_root(self, number: float) -> float:
        """Calculate square root of number"""
        if number < 0:
            raise ValueError("Square root of negative number is undefined for real numbers")
        result = math.sqrt(number)
        self._add_to_history(f"√({number})", result)
        return result
    
    @error_handler
    @timing_decorator
    @validate_input
    def cube_root(self, number: float) -> float:
        """Calculate cube root of number"""
        result = number ** (1/3)
        self._add_to_history(f"∛({number})", result)
        return result
    
    @error_handler
    @timing_decorator
    @validate_input
    def absolute(self, number: float) -> float:
        """Calculate absolute value of number"""
        result = abs(number)
        self._add_to_history(f"|{number}|", result)
        return result
    
    @error_handler
    @timing_decorator
    @validate_input
    def reciprocal(self, number: float) -> Union[float, str]:
        """Calculate reciprocal of number"""
        if number == 0:
            return "Error: Division by zero"
        result = 1 / number
        self._add_to_history(f"1/{number}", result)
        return result
    
    @error_handler
    @timing_decorator
    @validate_input
    def gamma_function(self, x: float) -> float:
        """Calculate gamma function of x"""
        result = math.gamma(x)
        self._add_to_history(f"Γ({x})", result)
        return result
    
    # ==================== STATISTICAL FUNCTIONS ====================
    def clear_statistical_data(self) -> None:
        """Clear all statistical data"""
        self.statistical_data = []
        self.regression_data = {'x': [], 'y': []}
    
    def add_data_point(self, value: float) -> None:
        """Add a data point to statistical data"""
        self.statistical_data.append(float(value))
    
    def add_regression_point(self, x: float, y: float) -> None:
        """Add a point for regression analysis"""
        self.regression_data['x'].append(float(x))
        self.regression_data['y'].append(float(y))
    
    @error_handler
    @timing_decorator
    def calculate_mean(self) -> Optional[float]:
        """Calculate mean of statistical data"""
        if not self.statistical_data:
            return None
        result = statistics.mean(self.statistical_data)
        self._add_to_history("mean(data)", result)
        return result
    
    @error_handler
    @timing_decorator
    def calculate_median(self) -> Optional[float]:
        """Calculate median of statistical data"""
        if not self.statistical_data:
            return None
        result = statistics.median(self.statistical_data)
        self._add_to_history("median(data)", result)
        return result
    
    @error_handler
    @timing_decorator
    def calculate_mode(self) -> Optional[float]:
        """Calculate mode of statistical data"""
        if not self.statistical_data:
            return None
        try:
            result = statistics.mode(self.statistical_data)
        except statistics.StatisticsError:
            result = None
        self._add_to_history("mode(data)", result)
        return result
    
    @error_handler
    @timing_decorator
    def calculate_standard_deviation(self, sample: bool = True) -> Optional[float]:
        """Calculate standard deviation of statistical data"""
        if not self.statistical_data:
            return None
        if sample and len(self.statistical_data) > 1:
            result = statistics.stdev(self.statistical_data)
        else:
            result = statistics.pstdev(self.statistical_data)
        self._add_to_history(f"stdev(data, sample={sample})", result)
        return result
    
    @error_handler
    @timing_decorator
    def calculate_variance(self, sample: bool = True) -> Optional[float]:
        """Calculate variance of statistical data"""
        if not self.statistical_data:
            return None
        if sample and len(self.statistical_data) > 1:
            result = statistics.variance(self.statistical_data)
        else:
            result = statistics.pvariance(self.statistical_data)
        self._add_to_history(f"variance(data, sample={sample})", result)
        return result
    
    @error_handler
    @timing_decorator
    def linear_regression(self) -> Optional[Dict[str, float]]:
        """Perform linear regression on regression data"""
        if len(self.regression_data['x']) < 2:
            return None
        
        x = self.regression_data['x']
        y = self.regression_data['y']
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi ** 2 for xi in x)
        sum_y2 = sum(yi ** 2 for yi in y)
        
        # Calculate slope (m) and intercept (b)
        denominator = n * sum_x2 - sum_x ** 2
        if denominator == 0:
            return None
        
        m = (n * sum_xy - sum_x * sum_y) / denominator
        b = (sum_y - m * sum_x) / n
        
        # Calculate correlation coefficient (r)
        numerator = n * sum_xy - sum_x * sum_y
        denominator_r = math.sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2))
        r = numerator / denominator_r if denominator_r != 0 else 0
        
        # Calculate R-squared
        r_squared = r ** 2
        
        result = {
            'slope': m,
            'intercept': b,
            'correlation': r,
            'r_squared': r_squared,
            'equation': f"y = {m:.6f}x + {b:.6f}"
        }
        
        self._add_to_history("linear_regression(x,y)", result)
        return result
    
    # ==================== FINANCIAL FUNCTIONS ====================
    @error_handler
    @timing_decorator
    @validate_input
    def future_value(self, rate: float, nper: int, pmt: float, pv: float = 0, 
                    type: int = 0) -> float:
        """
        Calculate future value of an investment
        
        Parameters:
        rate: Interest rate per period
        nper: Total number of payment periods
        pmt: Payment amount per period
        pv: Present value (initial investment)
        type: When payments are due (0 = end of period, 1 = beginning)
        """
        if rate == 0:
            fv = pv + pmt * nper
        else:
            fv = pv * (1 + rate) ** nper + pmt * (1 + rate * type) * ((1 + rate) ** nper - 1) / rate
        
        self._add_to_history(f"FV(rate={rate}, nper={nper}, pmt={pmt}, pv={pv})", fv)
        return fv
    
    @error_handler
    @timing_decorator
    @validate_input
    def present_value(self, rate: float, nper: int, pmt: float, fv: float = 0,
                     type: int = 0) -> float:
        """
        Calculate present value of an investment
        """
        if rate == 0:
            pv = -fv - pmt * nper
        else:
            pv = (-fv - pmt * (1 + rate * type) * ((1 + rate) ** nper - 1) / rate) / (1 + rate) ** nper
        
        self._add_to_history(f"PV(rate={rate}, nper={nper}, pmt={pmt}, fv={fv})", pv)
        return pv
    
    @error_handler
    @timing_decorator
    @validate_input
    def payment(self, rate: float, nper: int, pv: float, fv: float = 0,
               type: int = 0) -> float:
        """
        Calculate payment for a loan or investment
        """
        if rate == 0:
            pmt = (-pv - fv) / nper
        else:
            pmt = (rate * (fv + pv * (1 + rate) ** nper)) / ((1 + rate * type) * (1 - (1 + rate) ** nper))
        
        self._add_to_history(f"PMT(rate={rate}, nper={nper}, pv={pv}, fv={fv})", pmt)
        return pmt
    
    @error_handler
    @timing_decorator
    @validate_input
    def net_present_value(self, rate: float, cash_flows: List[float]) -> float:
        """
        Calculate net present value of a series of cash flows
        """
        npv = sum(cf / (1 + rate) ** i for i, cf in enumerate(cash_flows))
        self._add_to_history(f"NPV(rate={rate}, cash_flows={cash_flows})", npv)
        return npv
    
    # ==================== MATRIX OPERATIONS ====================
    @error_handler
    @timing_decorator
    def matrix_add(self, matrix_a: List[List[float]], matrix_b: List[List[float]]) -> List[List[float]]:
        """Add two matrices"""
        if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
            raise ValueError("Matrices must have the same dimensions")
        
        result = [[matrix_a[i][j] + matrix_b[i][j] for j in range(len(matrix_a[0]))] 
                  for i in range(len(matrix_a))]
        
        self._add_to_history("matrix_add(A, B)", result)
        return result
    
    @error_handler
    @timing_decorator
    def matrix_multiply(self, matrix_a: List[List[float]], matrix_b: List[List[float]]) -> List[List[float]]:
        """Multiply two matrices"""
        if len(matrix_a[0]) != len(matrix_b):
            raise ValueError("Number of columns in A must equal number of rows in B")
        
        result = [[sum(a * b for a, b in zip(row_a, col_b)) 
                   for col_b in zip(*matrix_b)] 
                  for row_a in matrix_a]
        
        self._add_to_history("matrix_multiply(A, B)", result)
        return result
    
    @error_handler
    @timing_decorator
    def matrix_transpose(self, matrix: List[List[float]]) -> List[List[float]]:
        """Transpose a matrix"""
        result = [[matrix[j][i] for j in range(len(matrix))] 
                  for i in range(len(matrix[0]))]
        
        self._add_to_history("matrix_transpose(A)", result)
        return result
    
    @error_handler
    @timing_decorator
    def matrix_determinant(self, matrix: List[List[float]]) -> float:
        """Calculate determinant of a matrix"""
        if len(matrix) != len(matrix[0]):
            raise ValueError("Matrix must be square")
        
        if len(matrix) == 1:
            return matrix[0][0]
        elif len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            # Use Laplace expansion for larger matrices
            determinant = 0
            for c in range(len(matrix)):
                submatrix = [[matrix[i][j] for j in range(len(matrix)) if j != c] 
                            for i in range(1, len(matrix))]
                sign = 1 if c % 2 == 0 else -1
                determinant += sign * matrix[0][c] * self.matrix_determinant(submatrix)
            
            return determinant
    
    # ==================== UNIT CONVERSIONS ====================
    @error_handler
    @timing_decorator
    @validate_input
    def convert_units(self, value: float, from_unit: str, to_unit: str, 
                     category: str) -> float:
        """
        Convert between different units
        
        Parameters:
        value: The value to convert
        from_unit: The unit to convert from
        to_unit: The unit to convert to
        category: The category of units (length, mass, temperature, etc.)
        """
        if category not in self.unit_conversions:
            raise ValueError(f"Unknown category: {category}")
        
        if from_unit not in self.unit_conversions[category] or to_unit not in self.unit_conversions[category]:
            raise ValueError(f"Unknown unit for category {category}")
        
        # Special handling for temperature
        if category == 'temperature':
            from_info = self.unit_conversions[category][from_unit]
            to_info = self.unit_conversions[category][to_unit]
            
            # Convert to Celsius first
            if from_info[0] != 'celsius':
                celsius_value = from_info[1](value)
            else:
                celsius_value = value
            
            # Convert from Celsius to target
            if to_info[0] != 'celsius':
                result = to_info[2](celsius_value)
            else:
                result = celsius_value
        else:
            # For other categories, use conversion factors
            from_factor = self.unit_conversions[category][from_unit]
            to_factor = self.unit_conversions[category][to_unit]
            result = value * from_factor / to_factor
        
        self._add_to_history(f"convert({value} {from_unit} to {to_unit})", result)
        return result
    
    # ==================== NUMBER SYSTEM CONVERSIONS ====================
    @error_handler
    @timing_decorator
    def convert_number_system(self, value: str, from_base: int, to_base: int) -> str:
        """
        Convert number between different bases
        
        Parameters:
        value: The number as a string
        from_base: The base of the input number (2-36)
        to_base: The base of the output number (2-36)
        """
        # Convert to decimal first
        decimal_value = int(value, from_base)
        
        # Convert to target base
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if decimal_value == 0:
            return "0"
        
        result = ""
        is_negative = decimal_value < 0
        decimal_value = abs(decimal_value)
        
        while decimal_value > 0:
            result = digits[decimal_value % to_base] + result
            decimal_value //= to_base
        
        if is_negative:
            result = "-" + result
        
        self._add_to_history(f"convert_base({value} from base {from_base} to base {to_base})", result)
        return result
    
    @error_handler
    @timing_decorator
    def binary_operations(self, a: str, b: str, operation: str) -> str:
        """
        Perform binary operations on binary numbers
        
        Parameters:
        a: First binary number as string
        b: Second binary number as string
        operation: Operation to perform (AND, OR, XOR, NOT, NAND, NOR, XNOR)
        """
        # Convert binary strings to integers
        int_a = int(a, 2) if a else 0
        int_b = int(b, 2) if b else 0
        
        # Perform operation
        if operation == "AND":
            result = int_a & int_b
        elif operation == "OR":
            result = int_a | int_b
        elif operation == "XOR":
            result = int_a ^ int_b
        elif operation == "NOT":
            result = ~int_a
        elif operation == "NAND":
            result = ~(int_a & int_b)
        elif operation == "NOR":
            result = ~(int_a | int_b)
        elif operation == "XNOR":
            result = ~(int_a ^ int_b)
        else:
            raise ValueError(f"Unknown binary operation: {operation}")
        
        # Convert back to binary string
        bits = max(len(a), len(b)) if operation not in ["NOT"] else len(a)
        mask = (1 << bits) - 1
        result &= mask  # Mask to appropriate number of bits
        
        binary_result = bin(result)[2:].zfill(bits)
        
        self._add_to_history(f"{operation}({a}, {b})", binary_result)
        return binary_result
    
    # ==================== DATE CALCULATIONS ====================
    @error_handler
    @timing_decorator
    def date_difference(self, date1: str, date2: str, 
                       format: str = "%Y-%m-%d") -> Dict[str, int]:
        """
        Calculate difference between two dates
        
        Parameters:
        date1: First date as string
        date2: Second date as string
        format: Date format string
        """
        d1 = datetime.datetime.strptime(date1, format)
        d2 = datetime.datetime.strptime(date2, format)
        
        if d1 > d2:
            d1, d2 = d2, d
