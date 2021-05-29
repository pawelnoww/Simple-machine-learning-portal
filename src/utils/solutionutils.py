def get_solution_dir():
    """
    Get Current Solutions Directory
    Returns
    -------
    str
        Application Path
    """
    from os import getcwd
    return getcwd().split('/src')[0] + '/'
