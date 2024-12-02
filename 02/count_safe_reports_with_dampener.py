MIN_DIFF = 1
MAX_DIFF = 3


def is_safe_report(report):
    """
    Checks if a single report is safe based on:
    - Levels being either all increasing or all decreasing.
    - Adjacent levels differing by at least MIN_DIFF and at most MAX_DIFF.
    """
    differences = [report[i + 1] - report[i] for i in range(len(report) - 1)]

    # Check for either all valid increases or all valid decreases
    return all(MIN_DIFF <= diff <= MAX_DIFF for diff in differences) or \
           all(-MAX_DIFF <= diff <= -MIN_DIFF for diff in differences)


def is_safe_report_with_dampener(report):
    """
    Checks if a single report is safe considering the Problem Dampener:
    - The report is safe if it's valid by the original rules.
    - If not, removing a single level from the report makes it safe.
    """
    if is_safe_report(report):
        return True

    # Try removing each level one at a time and check if the report becomes safe
    for i in range(len(report)):
        modified_report = report[:i] + report[i + 1:]
        if is_safe_report(modified_report):
            return True

    return False


def count_safe_reports_with_dampener(file_path):
    """
    Reads reports from a file and counts how many are safe considering the Problem Dampener.
    """
    with open(file_path, 'r') as file:
        reports = [list(map(int, line.split())) for line in file]
    return sum(is_safe_report_with_dampener(report) for report in reports)


def main():
    import sys

    # Ensure the user provides a file path as an argument
    if len(sys.argv) != 2:
        print("Usage: python count_safe_reports_with_dampener.py <input_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        # Count safe reports considering the Problem Dampener
        safe_count = count_safe_reports_with_dampener(file_path)
        print(f"The number of safe reports (with Problem Dampener) is: {safe_count}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
