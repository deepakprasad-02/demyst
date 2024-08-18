import csv
from file_processor import FileProcessor
from spec import Spec
import os


class DelimitedParser(FileProcessor):

    def process(self, spec: Spec, input_file_name: str, output_file_name: str) -> str:
        """
        Reads encoded file, parses it and generates .csv file.

        Args:
            spec (Spec): It details like whether to include a header, column names, and column offsets.
            input_file_name (str): name of the input file name to read from
            output_file_name (str): name of the file that it has to write out to

        Returns:
            file name of encoded file created
        """
        try:
            input_file_path = f"input_data/{input_file_name}"
            folder = "output_data"
            # Create the folder if it doesn't exist
            os.makedirs(folder, exist_ok=True)

            # Construct the full file path
            output_file_path = os.path.join(folder, output_file_name)

            with open(
                input_file_path, mode="r", encoding=spec.fixed_width_encoding
            ) as input_file, open(
                output_file_path, mode="w", newline="", encoding=spec.delimited_encoding
            ) as output_file:

                writer = csv.writer(output_file)

                # Iterate over each line in the fixed-width file
                for line in input_file:
                    row = []
                    start = 0

                    # Extract each field based on the specified offsets
                    for width in spec.offsets:
                        field = line[start : start + width].strip()
                        row.append(field)
                        start += width  # update the offset for next column data

                    writer.writerow(row)
            return "success"
        except Exception:
            print("error during parsing and csv file generation")
            raise Exception
