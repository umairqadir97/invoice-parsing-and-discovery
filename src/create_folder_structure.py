import os

# todo: update directory structure
directories = ['./data/', './data/delivery_challans/', './uploads/', './uploads/delivery_challans/']


def safe_make_folder(i):
    """Makes a folder (and its parents) if not present"""
    try:  
        os.makedirs(i)
    except:
        pass


if __name__ == "__main__":
    for directory in directories:
        safe_make_folder(directory)
