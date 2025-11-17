from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DB_URL = "sqlite:///pm_agent.db"
engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

Base = declarative_base()

class BRD(Base):
    __tablename__ = "brds"
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    runs = relationship("Run", back_populates="brd")

class Run(Base):
    __tablename__ = "runs"
    id = Column(Integer, primary_key=True)
    brd_id = Column(Integer, ForeignKey("brds.id"), nullable=False)
    clarify_meta = Column(JSON)   # meta object
    questions = Column(JSON)      # list of questions
    answers = Column(JSON)        # dict {Qid: answer}
    stories = Column(JSON)        # final stories JSON

    brd = relationship("BRD", back_populates="runs")
