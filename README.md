[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
    <img src="reports/invoices-logo.jpg" alt="Logo" width="512" height="256">
  </a>

  <h3 align="center">Invoices Parsing & Discovery</h3>

  <p align="center">
    This system intends to solve the problem of parsing and mapping hundreds of thousands invoices to respective delivery challans and purchase orders, automatically.
    <br />
    <br />
    <br />
    <a href="mailto:umairqadir97@gmail.com">Request Demo</a>
    ·
    <a href="https://github.com/umairqadir97/invoice-parsing-and-discovery/issues">Report Bug</a>
    ·
    <a href="https://github.com/umairqadir97/invoice-parsing-and-discovery/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-main-screenshot]](#about-the-project)

[![Product Name Screen Shot][product-progress-screenshot]](#about-the-project) -->

<div>
<iframe width="560" height="315" src="https://www.youtube.com/embed/iAtMRl2IumY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>



Data-Warehouse related project for fetching, parsing and mapping commercial invoices with relevant delivery-challan & purchase-order. Parsing the Purchase Orders, Delivery Challans & preparing mappings.


<br>


**Top 3 Key Learning:**
* Setting up boilerplates for flask project
* POc development with Flask templates
* Data-warehousing

This project is still in development. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue.

[Contributors are always welcomed!](#contributing)

<br>

### Built With

* [Python](http://python.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Pandas](https://pandas.pydata.org/)
* [Numpy](https://numpy.org/)
* [PdfQuery](https://pypi.org/project/pdfquery/)
* [Tabula-Py](https://pypi.org/project/tabula-py/)
* [Json2html](https://pypi.org/project/json2html/)
* [FuzzyWuzzy](https://pypi.org/project/fuzzywuzzy/)


<!-- GETTING STARTED -->
## Getting Started


To get a local copy up and running follow these simple example steps.

### Prerequisites

To run this project,  you should have following dependencies ready:

1. Python3
2. pip


<br>

### Installation

Open terminal in root directory, and execute following commands:

1) ```pip3 install -r requirements.txt```

2) ```pyhon3 create_folder_structure.py```

3) ```python3 api.py```

Open in browser [API](http://127.0.0.1:5000/), and you are done !


1. Clone the repo
```sh
git clone https://github.com/umairqadir97/invoice-parsing-and-discovery.git
```
2. Open terminal in project folder
```sh 
cd invoice-parsing-and-discovery
```

3. Install python packages
```sh
pip3 install -r requirements.txt
```

4. Create required directory structure with following script
```sh
pyhon3 create_folder_structure.py
```

5. Run flask server
```sh
python3 api.py
```

6. Visit URL

Open [API](http://127.0.0.1:5000/) in browser, and you are done!


<br>

<!-- Project Organization -->

## Project Organization
------------

    ├── LICENSE
    ├── README.md                       <- The top-level README for developers using this project.
    ├── data
    │   ├── delivery_challans           <- ...
    │   └── * files
    │
    ├── uploads             <- ...
    │
    ├── notebooks          <- Jupyter notebooks for experimentation.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    |
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    |	|── * files

<br>

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/umairqadir97/invoice-parsing-and-discovery/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b amazing_features`)
3. Commit your Changes (`git commit -m 'Add some Amazing Features'`)
4. Push to the Branch (`git push origin amazing_features`)
5. Open a Pull Request


### Contribution guidelines
1. Writing tests
2. Code review
3. Feature Enhancement

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

**Muhammad Umair Qadir**

Catch me on [Email](umairqadir97@gmail.com)

Get Connected on [LinkedIn](https://linkedin.com/in/umairqadir)





<!-- MARKDOWN LINKS & IMAGES -->

<!-- Contributors -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=flat-square
[contributors-url]: https://github.com/umairqadir97/invoice-parsing-and-discovery/graphs/contributors

<!-- Issues -->
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=flat-square
[issues-url]: https://github.com/umairqadir97/invoice-parsing-and-discovery/issues

<!-- Lisence -->
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/umairqadir97/invoice-parsing-and-discovery/blob/master/LICENSE.txt

<!-- LinkedIn -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/umairqadir

<!-- Product Screenshot -->
[product-main-screenshot]: reports/about-invoice-parsing.png
[product-progress-screenshot]: reports/progress-bar.png
