# Scanipy: Deep Learning-Powered PDF Scanning and Parsing

![Scanipy logo oficial](https://github.com/SVJLucas/Scanipy/assets/60625769/554bd0b6-6f88-4226-a1bc-43dcfa62fd0b)

**Scanipy** stands for "scan it with Python"—it's your smart Python library for **scanning and parsing complex PDF files** like books, reports, articles, and academic papers. Utilizing cutting-edge **Deep Learning** algorithms, Scanipy transforms your PDFs into a treasure trove of extractable information: **tables, images, equations, and text**. Say goodbye to manual scanning tasks and hello to automated, intelligent data extraction.

## Example

🚨 **The code is still under development, but it should be fully functional by September 29, 2023.** 🚨

Run with

```python
import scanipy

parser = scanipy.Parser()
document = parser.extract("test.pdf")
document.to_markdown(output_folder="output")
```

Visualize the extracted blocks with

```python
document.visualize_pipeline(page=0, step=0)
```
