import scanipy

def main():
    parser = scanipy.Parser()
    document = parser.extract("test.pdf")
    document.to_markdown('output')

if __name__ == "__main__":
    main()
