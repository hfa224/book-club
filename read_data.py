import csv

def read_book_data() :
  with open('static/data/Berlin Beer & Book Club.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[2]} picked {row[0]} by {row[1]} in {row[3]}.')
            line_count += 1
    print(f'Processed {line_count} lines.')
    
def get_book_image_url(isbn):
  return "https://covers.openlibrary.org/b/isbn/" + isbn + "-M.jpg";
    
def read_book_isbns() :
  with open('static/data/Berlin Beer & Book Club.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[2]} picked {row[0]} by {row[1]} in {row[3]}.')
            line_count += 1
    print(f'Processed {line_count} lines.')