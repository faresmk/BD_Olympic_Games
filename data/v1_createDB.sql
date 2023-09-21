-- TODO 1.3a : Créer les tables manquantes et modifier celles ci-dessous
CREATE TABLE LesDisciplines
(
    nomDi VARCHAR2(30) NOT NULL,
    CONSTRAINT DI_PK PRIMARY KEY(nomDi)
);

CREATE TABLE LesParticpants 
(
  numPa NUMBER (4),
  CONSTRAINT PR_PK PRIMARY KEY(numPa),
  CONSTRAINT PR_CK CHECK ((numPa > 0 and numPa < 100) or (numPa > 1000 and numPa < 1500))
);



CREATE TABLE LesSportifs_base
(
  numSp NUMBER(4),
  nomSp VARCHAR2(20) NOT NULL,
  prenomSp VARCHAR2(20) NOT NULL,
  pays VARCHAR2(20) NOT NULL,
  categorieSp VARCHAR2(10),
  dateNaisSp DATE,
  numEq NUMBER(4),
  CONSTRAINT SP_PK PRIMARY KEY(numSp),
  CONSTRAINT SP_FK FOREIGN KEY (numSp) REFERENCES LesParticipant(numPa) ON DELETE CASCADE,
  CONSTRAINT SP_CK1 CHECK(numSp > 0),
  CONSTRAINT SP_CK2 CHECK(categorieSp IN ('feminin','masculin')),
  CONSTRAINT SP_CK3 CHECK(numEq > 0)
);


CREATE TABLE LesEquipes_base
(
    numEq NUMBER (4) ,
    CONSTRAINT EQB_PK PRIMARY KEY(numEq),
    CONSTRAINT EQB_FK FOREIGN KEY (numEq) REFERENCES LesParticipant(numPa) ON DELETE CASCADE 
);

CREATE TABLE MembreEQ
(
    numEq INTEGER,
    numSp INTEGER,

    CONSTRAINT MEQ_PK PRIMARY KEY (numEq, numSp),
    FOREIGN KEY (numEq) REFERENCES LesEquipes_base(numEq) ON DELETE CASCADE,
    FOREIGN KEY (numSp) REFERENCES LesSportifs_base(numSp) ON DELETE CASCADE
);



CREATE TABLE LesEpreuves
(
  numEp NUMBER(3),
  nomEp VARCHAR2(20),
  formeEp VARCHAR2(13),
  nomDi VARCHAR2(25),
  categorieEp VARCHAR2(10),
  nbSportifsEp NUMBER(2),
  dateEp DATE,
  CONSTRAINT EP_PK PRIMARY KEY (numEp),
  CONSTRAINT EP_FK FOREIGN KEY (nomDi) REFERENCES LesDisciplines(nomDi) ON DELETE CASCADE ,
  CONSTRAINT EP_CK1 CHECK (formeEp IN ('individuelle','par equipe','par couple')),
  CONSTRAINT EP_CK2 CHECK (categorieEp IN ('feminin','masculin','mixte')),
  CONSTRAINT EP_CK3 CHECK (numEp > 0),
  CONSTRAINT EP_CK4 CHECK (nbSportifsEp > 0)
);


CREATE TABLE LesResultats
(
    numEp NUMBER(5) ,
    gold  NUMBER(5) NOT NULL,
    silver NUMBER(5) NOT NULL,
    bronze NUMBER(5) NOT NULL,
    CONSTRAINT RS_PK PRIMARY KEY (numEp),
    CONSTRAINT RS_FK FOREIGN KEY (numEp) REFERENCES LesEpreuve(numEp) ON DELETE CASCADE,
    CONSTRAINT RS_FK1  FOREIGN KEY (gold) REFERENCES LesParticpants(numPa),
    CONSTRAINT RS_FK2 FOREIGN KEY  (silver) REFERENCES LesParticpants(numPa),
    CONSTRAINT RS_FK3 FOREIGN KEY (bronze) REFERENCES LesParticpants(numPa)
);

CREATE TABLE LesInscriptions
(
 numIn NUMBER(4),
 numEp NUMBER(4),
 CONSTRAINT INS_FK FOREIGN KEY (numEp) REFERENCES LesEpreuves(numEp) ,
 CONSTRAINT INS_FK FOREIGN KEY (numIn) REFERENCES LesParticipant(numPa)
);
-- TODO 1.4a : ajouter la définition de la vue LesAgesSportifs
DROP VIEW IF EXISTS LesAgesSportifs;
CREATE VIEW IF NOT EXISTS LesAgesSportifs
AS
SELECT numSp,
       nomSp,
       prenomSp,
       pays,
       categorieSp,
       (DATE('now') - dateNaisSp)  AS Age,
       numEq
          FROM LesSportifs_base;

-- TODO 1.5a : ajouter la définition de la vue LesNbsEquipiers
DROP VIEW IF EXISTS LesNbsEquipiers;
CREATE VIEW IF NOT EXISTS LesNbsEquipiers
AS
SELECT numEq, COUNT(numSp) AS NbsEquipiers
FROM MembreEQ
GROUP BY numEq;