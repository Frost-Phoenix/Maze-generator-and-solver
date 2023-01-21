def init() -> list:
    return []

def est_vide(P: list) -> bool:
    return len(P) == 0

def empile(P, val: any) -> None:
    P.append(val)

def depile(P: list) -> any:
    assert est_vide(P) == False
    return P.pop()