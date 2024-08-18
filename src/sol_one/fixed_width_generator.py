import random
import os
import string
from file_processor import FileProcessor
from spec import Spec


class FixedWidthGenerator(FileProcessor):
    def process(self, spec: Spec, num_rows: int = 10) -> str:
        """
        creates fake dataset, encodes it and generates .txt file.

        Args:
            spec (Spec): It details like whether to include a header, column names, and column offsets.
            num_rows (int): It is number of data rows to generate in the dataset,
                            default is 10 rows of data.

        Returns:
            file name of encoded file created
        """
        try:
            # create fake data
            dataset = self._get_fake_dataset(spec, num_rows)

            # Convert the data to Windows-1252 encoding
            encoded_data = [row.encode(spec.fixed_width_encoding) for row in dataset]

            # Write the data to a file
            file_name = "fixed_width_data.txt"
            folder = "input_data"
            # Create the folder if it doesn't exist
            os.makedirs(folder, exist_ok=True)

            # Construct the full file path
            file_path = os.path.join(folder, file_name)

            with open(file_path, "wb") as file:
                for row in encoded_data:
                    file.write(row + b"\n")

            return file_name
        except Exception:
            raise "unexpected error encountered during file generation"

    def _get_fake_dataset(self, spec: Spec, num_rows: int) -> list:
        """
        Generates a fake dataset based on the provided specification.

        Args:
            spec (Spec): It details like whether to include a header, column names, and column offsets.
            num_rows (int): It is number of data rows to generate in the dataset.

        Returns:
            A list of strings representing the dataset
        """
        data = []
        # includes headers if required
        if spec.include_header:
            header = self._generate_header(spec.column_names, spec.offsets)
            data.append(header)

        for _ in range(num_rows):
            row = self._generate_data_row(spec.offsets)
            data.append(row)

        return data

    def _generate_random_data(self, width) -> str:
        """
        Generates a random string of alphanumeric characters.

        Args:
            width (int): The length of the random string to generate.

        Returns:
            A string of randomly selected alphanumeric characters of the
                specified length.
        """
        return "".join(random.choices(string.ascii_letters + string.digits, k=width))

    def _generate_data_row(self, offsets: list) -> str:
        """
        Generates a random list of alphanumeric strings.

        Args:
            offsets (int): The length of the each column to generate.

        Returns:
            A list of randomly generated alphanumeric strings.
        """
        return "".join([self._generate_random_data(length) for length in offsets])

    # Generate the header based on the column names and offsets
    def _generate_header(self, column_names: list, offsets: list):
        """
        Generates a random list of alphanumeric strings.

        Args:
            offsets (int): The length of the each column to generate.

        Returns:
            A list of randomly generated alphanumeric strings.
        """
        header = ""
        for name, offset in zip(column_names, offsets):
            # Truncate or pad the column name to fit the offset
            if len(name) > offset:
                header += name[:offset]
            else:
                header += name.ljust(offset)
        return header
