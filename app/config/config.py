import os
import logging

from flask import jsonify

from logging.handlers import RotatingFileHandler
class ConfigDev:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://aly:ORcKRINPV072ZZnkyspFBMqubDtxfAml@dpg-d503i6c9c44c73d9mvm0-a.virginia-postgres.render.com:5432/db_vente"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "20µµ%§.KLKKJ000")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "###MMLL2233.0KKKSS")


class ConfigUat:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:NouveauMotDePasse@localhost:5432/db_vente"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "20µµ%§.KLKKJ000")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "###MMLL2233.0KKKSS")


class ConfigProd:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:NouveauMotDePasse@localhost:5432/db_vente"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "20µµ%§.KLKKJ000")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "###MMLL2233.0KKKSS")

config_dict={
    'dev':ConfigDev,
    'test':ConfigUat,
    'prod':ConfigProd
}