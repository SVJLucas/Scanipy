import scanipy

parser = scanipy.Parser()
document = parser.extract("test.pdf")
document.to_markdown('output')
