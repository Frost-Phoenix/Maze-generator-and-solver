def init() -> list:
    return []

def est_vide(F: list) -> bool:
    return len(F) == 0

def emfile(F, val: any) -> None:
    F.append(val)

def defile(F: list) -> any:
    assert est_vide(F) == False
    return F.pop(0)