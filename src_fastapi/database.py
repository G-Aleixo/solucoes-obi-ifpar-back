from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, sessionmaker, mapped_column, relationship

sqlite_file_name = "instance/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    ...


class TestPair(Base):
    __tablename__ = "testpairs"

    id: Mapped[int] = mapped_column(primary_key=True)
    subtask_id: Mapped[int] = mapped_column(ForeignKey("subtasks.id"), primary_key=True, nullable=False)
    
    installed: Mapped[bool] = mapped_column(nullable=False)
    input: Mapped[str] = mapped_column(nullable=True)
    output: Mapped[str] = mapped_column(nullable=True)
    
    subtask: Mapped["SubTask"] = relationship(back_populates="subtasks")

class SubTask(Base):
    __tablename__ = "subtasks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"), primary_key=True, nullable=False)
    
    subtasks: Mapped[List["TestPair"]] = relationship(back_populates="subtask")
    
    problem: Mapped["Problem"] = relationship(back_populates="subtasks")

class Problem(Base):
    __tablename__ = "problems"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    year: Mapped[str] = mapped_column()
    phase: Mapped[str] = mapped_column()
    level: Mapped[str] = mapped_column()
    
    subtasks: Mapped[List["SubTask"]] = relationship(back_populates="problem")