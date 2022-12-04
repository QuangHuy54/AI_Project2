from resolution_algorithm import read_input_from_file, export_output_to_file, PL_RESOLUTION
import os

def main():
    for inputfile in os.listdir("./INPUT"):
        inputPath = os.path.join("./INPUT", inputfile)
        outputPath = inputPath.replace("INPUT", "OUTPUT").replace("input", "output")
        KB, alpha = read_input_from_file(inputPath)
        result, entail = PL_RESOLUTION(KB, alpha)
        export_output_to_file(outputPath, result, entail)

main()
