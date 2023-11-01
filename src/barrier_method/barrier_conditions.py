
from dataclasses import dataclass, field
from typing import Dict, Callable

@dataclass
class BarrierConditions:
    """
    A class that generates and manages barrier conditions used for different labeling techniques.
    Those conditions can be used to generate labels like this. Example for n=1:
        y = 
            -1 if r_{t,t+n} < -barrier,
             1 if  r_{t,t+n} > -barrier,
             0 else
    Different n will add conditions by multiples of barrier up to n-multiples.

    Attributes:
    n (int): The number of barrier conditions to be generated for negative and positive barriers.
    barrier (float): The threshold value for the barrier.
    conditions (Dict[int, Callable[[float], bool]]): A dictionary holding condition functions for various barrier levels. Keys are sorted numerically.
    """
    n: int
    barrier: float
    conditions: Dict[int, Callable[[float], bool]] = field(default_factory=dict)

    def __post_init__(self):
        """
        Calculate the conditions after the instance has been initialized.
        """
        self.generate_conditions()
        self.sort_conditions()
    
    def generate_conditions(self):
        """
        Generates barrier conditions based on the specified number of conditions and threshold values.
        """
        for i in range(1, self.n+1):
            self.conditions[-i] = self._negative_condition(i)
            self.conditions[i] = self._positive_condition(i)

    def _negative_condition(self, i):
        return lambda x: x < -1*i*self.barrier
    
    def _positive_condition(self, i):
        return lambda x: x > i*self.barrier

    def sort_conditions(self):
        """
        Sorts the generated conditions in ascending order based on their keys.
        """
        self.conditions = dict(sorted(self.conditions.items()))
