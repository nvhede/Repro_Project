import csv
import sys

#all caps usually designates a global variable
MY_FILE = "/incident.csv.txt"

def parse (raw_file, delimiter = ','):
    """Parses a raw CSV/Excel File to a JSON-line object."""
    #open file
    opened_file = open (raw_file)
    #read file
    #first delimiter -> argument of csv.reader.
    #second delimiter -> argument of our parse function.
    csv_data = csv.reader (opened_file, delimiter = delimiter)
    #build a data structure to return parsed_data
    parsed_data = []
    fields = csv_data.next () #for the column headers
    for row in csv_data: #assigns a value to each header
        parsed_data.append (dict(zip(fields,row)))
    #close file
    opened_file.close ()
    return parsed_data

def main ():
    """calls our parse function and sees what the data looks like"""
    new_data = parse(MY_FILE, ",")
    print new_data
    saveParse ()


def saveParse ():
    """Takes the parsed data and saves it to  a new file."""
    with open ('parsedfile.txt', 'w') as new_data:
        parsed_stuff = parse (MY_FILE, ',')
        new_data.write (str(parsed_stuff))



if __name__ == "__main__":
    main ()
