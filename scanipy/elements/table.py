from typing import Union
import pandas as pd
from .element import Element

# Define the TableElement class
class TableElement(Element):
    """
    Represents a table element within a document for displaying tabular data.

    Attributes:
        table_data (pandas.DataFrame): The DataFrame containing the tabular data.
    """

    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int, 
                 pipeline_step: Union[int, None] = None):
        """
        Initialize a TableElement object.

        Args:
            x_min (int): The minimum x-coordinate.
            y_min (int): The minimum y-coordinate.
            x_max (int): The maximum x-coordinate.
            y_max (int): The maximum y-coordinate.
            pipeline_step (Union[int, None], optional): The pipeline step, can be None.

        Raises:
            TypeError: If the types of the arguments are not as expected.
        """
        # Verify the input variable types
        if not all(isinstance(var, int) for var in [x_min, y_min, x_max, y_max]):
            raise TypeError("Coordinates must be integers")
        if pipeline_step is not None and not isinstance(pipeline_step, int):
            raise TypeError("pipeline_step must be an integer or None")

        # Initialize instance variables by calling the parent class constructor
        super().__init__(x_min, y_min, x_max, y_max, pipeline_step)

        # Initialize additional instance variable specific to TableElement
        self._table_data = None

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

    def __str__(self) -> str:
        """
        Returns a string representation of the TableElement object.

        Returns:
            str: A string representation of the object.
        """
        return f"TableElement(x_min={self.x_min}, y_min={self.y_min}, x_max={self.x_max}, y_max={self.y_max}, pipeline_step={self.pipeline_step}, table_data={self.table_data})"

    def generate_markdown(self, output_directory: str) -> str:
        """
        Generate the Markdown representation of the table element.

        Args:
            output_directory (str): The directory where the table will be saved.

        Returns:
            str: Markdown representation of the table element.
        """
        # Convert the DataFrame to Markdown format
        formatted_table = self.table_data.to_markdown() + '\n\n'
        return formatted_table
