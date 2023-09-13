from .element import Element


class TableElement(Element):
    """
    Represents a table element for printing tabular data.

    Attributes:
    df (pandas.DataFrame): The DataFrame containing tabular data.

    Methods:
    print(output_folder):
        Returns the formatted table for printing to an output folder.

    """

    def __init__(self, x_min, y_min, x_max, y_max, pipeline_step, df):
        """
        Initializes a new TableElement.

        Parameters:
        df (pandas.DataFrame): The DataFrame containing tabular data.
        """
        super().__init__(x_min, y_min, x_max, y_max, pipeline_step)
        self.df = df

    def print(self, output_folder):
        """
        Generates the formatted table for printing.

        Parameters:
        output_folder (str): The path to the output folder.

        Returns:
        str: The formatted table.
        """
        response = self.df.to_markdown() + '\n\n'
        return response
