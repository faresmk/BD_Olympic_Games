-- TODO 3.3 Créer un trigger pertinent

-- Les sportifs d'une équipe doivent étre du meme pays
DROP TRIGGER IF EXISTS MembreEquipePays;
CREATE TRIGGER MembreEquipePays
    BEFORE INSERT ON MembreEQ
    WHEN NOT EXISTS (SELECT pays FROM LesSportifs_base join MembreEQ using (numSp) WHERE NEW.numEq = MembreEQ.numEq AND pays IN (SELECT pays FROM LesSportifs_base WHERE numSp = NEW.numSp))
BEGIN
    SELECT RAISE (ABORT, 'Les sportifs d une meme equipe doivent etre du meme pays ');
END;