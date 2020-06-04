from src.api_helper import *

if __name__ == "__main__":
    pos_input_directory = "/home/umair/redbuffer/fatima_group_invoices/merged_pos/"
    benchmark_output_directory = "/home/umair/redbuffer/invoice_matching/data/"
    write_to_file = True

    benchmark_for_all_pos(input_directory=pos_input_directory,
                          output_directory=benchmark_output_directory,
                          write_to_file=write_to_file)
