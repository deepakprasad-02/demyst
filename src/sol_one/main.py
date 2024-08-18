from file_processor import FileProcessor
from fixed_width_generator import FixedWidthGenerator
from csv_generator import DelimitedParser
from spec import Spec


class FileProcessorFactory:
    @staticmethod
    def get_processor(processor_type: str) -> FileProcessor:
        """
        Factory method that returns specific object for the type of tasks(parsing) implemented.

        Args:
            processor_type (Spec): limited string values that channel to the type of task.

        Returns:
            object of required parsing

        Raises:
            Value error if unimplemented strings are passed
        """
        if processor_type == "fixed_width_generator":
            return FixedWidthGenerator()
        elif processor_type == "delimited_parser":
            return DelimitedParser()
        else:
            raise ValueError(f"Unsupported processor type: {processor_type}")


def main():
    spec = Spec.from_json("spec.json")

    generator = FileProcessorFactory.get_processor("fixed_width_generator")
    generated_input_file_name = generator.process(spec)

    parser = FileProcessorFactory.get_processor("delimited_parser")
    output_message = parser.process(
        spec=spec,
        input_file_name=generated_input_file_name,
        output_file_name="output.csv",
    )
    print(output_message)


if __name__ == "__main__":
    main()
