## invoice-parsing-and-discovery
Data-Warehouse related project for fetching, parsing and mapping commercial invoices with relevant delivery-challan & purchase-order.




(Purchase Order <==> Delivery Challans) Parsing & Mapping 
==============================

Parsing the Purchase Orders, Delivery Challans & preparing mappings.

[Project Documentation]

Project Organization
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



Setup Project
------------
Open terminal in root directory, and execute following commands:

1) ```pip3 install -r requirements.txt```

2) ```pyhon3 create_folder_structure.py```

3) ```python3 api.py```

Open in browser [API](http://127.0.0.1:5000/), and you are done !
