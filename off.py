import re

a = "datetime.datetime(2022, 12, 7, 19, 42, 36),22.0,'trés sec')"
pattern = "\d{1,4}"
print(re.findall(pattern,a))