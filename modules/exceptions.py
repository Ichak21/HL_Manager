class ErreurRM6Existe(Exception):
    def __init__(self, rm6, message="Le RM6 existe déjà sans date de sortie"):
        self.rm6 = rm6
        self.message = f"{message}: {rm6}"
        super().__init__(self.message)