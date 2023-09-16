from typing import Union
import logging
from .element import Element
from .equation import EquationElement


# Define the TitleElement class
class TitleElement(Element):
    """
    Represents a title element within a document.

    Attributes:
        title_content (str): The content of the title element.
        has_equation_inside (bool): If there's some equation inside the title.
    """

    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float, 
                 pipeline_step: Union[int, None] = None, page_number: Union[int, None] = None):
        """
        Initialize a TitleElement object.

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

        # Initialize additional instance variable specific to TitleElement
        self._title_content = None
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
        
    # Setter and Getter for title_content
    @property
    def title_content(self) -> Union[str, None]:
        """
        Gets the content of the title element.

        Returns:
            Union[str, None]: The content of the title element.
        """
        return self._title_content

    @title_content.setter
    def title_content(self, value: Union[str, None]):
        """
        Sets the content of the title element.

        Args:
            value (Union[str, None]): The new content for the title element.

        Raises:
            TypeError: If the provided value is not a string or None.
        """
        if value is not None and not isinstance(value, str):
            raise TypeError("title_content must be a string or None")
        self._title_content = value

    def __str__(self) -> str:
        """
        Returns a string representation of the TitleElement object.

        Returns:
            str: A string representation of the object.
        """
        return f"TitleElement(x_min={self.x_min}, y_min={self.y_min}, x_max={self.x_max}, y_max={self.y_max}, pipeline_step={self.pipeline_step}, title_content={self.title_content}, has_equation_inside={self.has_equation_inside})"

    def __str__(self)-> str:
        """
        Returns a string representation of the object, which is the same as its official representation.
        
        Returns:
            str: A string that can be used to recreate the object.
        """
        return self.__repr__()
    
    def generate_markdown(self, output_directory: str) -> str:
        """
        Generate the Markdown representation of the title element.

        Args:
            output_directory (str): The directory where the text file will be saved.

        Returns:
            str: Markdown representation of the title element.
        """
        if self.title_content == None:
            logging.warning('Tried to write a NoneType object')
            return '\n\n'

        # Add Markdown header formatting to the title content
        formatted_title = '## ' + self.title_content + '\n\n'
        return formatted_title
