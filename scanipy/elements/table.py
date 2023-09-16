import logging
from typing import Union
import pandas as pd
from .element import Element
from .equation import EquationElement

# Define the TableElement class
class TableElement(Element):
    """
    Represents a table element within a document for displaying tabular data.

    Attributes:
        table_data (pandas.DataFrame): The DataFrame containing the tabular data.
        has_equation_inside (bool): If there's some equation inside the table.
    """

    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float, 
                 pipeline_step: Union[int, None] = None, page_number: Union[int, None] = None):
        """
        Initialize a TableElement object.

        Args:
            x_min (float): The minimum x-coordinate of the element, normalized to the image width (range: 0 to 1).
            y_min (float): The minimum y-coordinate of the element, normalized to the image height (range: 0 to 1).
            x_max (float): The maximum x-coordinate of the element, normalized to the image width (range: 0 to 1).
            y_max (float): The maximum y-coordinate of the element, normalized to the image height (range: 0 to 1).
            pipeline_step (Union[int, None], optional): The pipeline step, can be None.
            page_number (int): Specifies the page number on which the element is located.

        Raises:
            TypeError: If the types of the arguments are not as expected.
        """
                     
        # Initialize instance variables by calling the parent class constructor
        super().__init__(x_min, y_min, x_max, y_max, pipeline_step, page_number)

        # Initialize additional instance variable specific to TableElement
        self._table_data = None
        self._has_equation_inside = False
        self._equation_inside = None
        
    @property
    def equation_inside(self) -> Union[EquationElement,None]:
        """
        Get the equation inside the element, if any.
    
        Returns:
            EquationElement if the element contains equations, otherwise None.
        """
        return self._equation_inside

    @equation_inside.setter
    def equation_inside(self, value: EquationElement):
        """
        Sets the equation inside the element.

        Args:
            value (EquationElement): The new EquationElement value.

        Raises:
            TypeError: If the provided value is not a EquationElement.
        """
        if not isinstance(value, EquationElement):
            raise TypeError("equation_inside must be a EquationElement")
        self._equation_inside = value

    @property
    def has_equation_inside(self) -> bool:
        """
        Determines if the element contains equations.
    
        This method checks if the element has any equations inside it and returns a boolean value accordingly.
    
        Returns:
            bool: True if the element contains equations, otherwise False.
        """
        return self._has_equation_inside

    @has_equation_inside.setter
    def has_equation_inside(self, value: bool):
        """
        Sets a boolean that checks if the element has any equations inside it.

        Args:
            value (bool): The new boolean value.

        Raises:
            TypeError: If the provided value is not a bool.
        """
        if not isinstance(value, bool):
            raise TypeError("has_equation_inside must be a bool")
        self._has_equation_inside = value
        
    # Setter and Getter for table_data
    @property
    def table_data(self) -> Union[pd.DataFrame, None]:
        """
        Gets the DataFrame containing the tabular data.

        Returns:
            Union[pd.DataFrame, None]: The DataFrame containing the tabular data.
        """
        return self._table_data

    @table_data.setter
    def table_data(self, value: Union[pd.DataFrame, None]):
        """
        Sets the DataFrame containing the tabular data.

        Args:
            value (Union[pd.DataFrame, None]): The new DataFrame for the table element.

        Raises:
            TypeError: If the provided value is not a DataFrame or None.
        """
        if value is not None and not isinstance(value, pd.DataFrame):
            raise TypeError("table_data must be a pandas DataFrame or None")
        self._table_data = value

    def __repr__(self) -> str:
        """
        Returns a string representation of the TableElement object.

        Returns:
            str: A string representation of the object.
        """
        return f"TableElement(x_min={self.x_min}, y_min={self.y_min}, x_max={self.x_max}, y_max={self.y_max}, pipeline_step={self.pipeline_step}, table_data={self.table_data}, has_equation_inside={self.has_equation_inside})"

    def __str__(self):
        """
        Returns a string representation of the object, which is the same as its official representation.
        
        Returns:
            str: A string that can be used to recreate the object.
        """
        return self.__repr__()

    def generate_markdown(self, output_directory: str) -> str:
        """
        Generate the Markdown representation of the table element.

        Args:
            output_directory (str): The directory where the table will be saved.

        Returns:
            str: Markdown representation of the table element.
        """
        if self.table_data == None:
            logging.warning('Tried to write a NoneType object')
            return '\n\n'

        # Convert the DataFrame to Markdown format
        formatted_table = self.table_data.to_markdown() + '\n\n'
        return formatted_table
