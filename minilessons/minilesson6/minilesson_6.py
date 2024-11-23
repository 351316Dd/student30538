add = lambda x, y: x + y
print(add(5, 3))

# Using map()
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(squared)  # Output: [1, 4, 9, 16, 25]

# Using filter()
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # Output: [2, 4]

# Without Lambda Functions
def myfunc_no_lambda(n):
    def multiplier(a):
        return a * n
    return multiplier

mytripler1 = myfunc_no_lambda(3)

print(mytripler1(12))

# With Lambda Functions
def myfunc_with_lambda(n):
  return lambda a : a * n

mytripler2 = myfunc_with_lambda(3)

print(mytripler2(12))

from bs4 import BeautifulSoup

html_doc = """
<html>
  <body>
    <p>Python is a great programming language.</p>
    <p>JavaScript is also popular.</p>
    <p>Python can be used for web scraping.</p>
  </body>
</html>
"""
soup = BeautifulSoup(html_doc, 'html.parser')
# Use lambda to find all <p> tags that contain the word "Python"
python_paragraphs = soup.find_all('p', string=lambda text: 'Python' in text)

for p in python_paragraphs:
    print(p.text)

html_doc = """
<html>
  <body>
    <a href="https://www.example.com">Example Site</a>
    <a href="https://www.another.com">Another Site</a>
    <a href="https://example.org">Example Organization</a>
  </body>
</html>
"""

soup = BeautifulSoup(html_doc, 'html.parser')

# Use lambda to find all <a> tags where href contains "example"
example_links = soup.find_all('a', href=lambda href: href and 'example' in href)

for link in example_links:
    print(link['href'])
