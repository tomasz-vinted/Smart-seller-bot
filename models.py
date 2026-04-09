from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class UserAction(Base):
    __tablename__ = 'user_actions'
    id = Column(Integer, primary_key=True)
    platform_user_id = Column(String, unique=True) # ID użytkownika na Vinted/OLX
    username = Column(String)
    item_id = Column(String)
    item_name = Column(String)
    action_type = Column(String) # e.g., 'offer_sent', 'message_sent'
    timestamp = Column(DateTime, default=datetime.utcnow)

class BotConfig(Base):
    __tablename__ = 'bot_config'
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=False)
    discount_amount = Column(Float, default=5.0)
    openai_token = Column(String)
    telegram_token = Column(String)
    telegram_chat_id = Column(String)
    platform_session_cookie = Column(Text) # Przechowywanie sesji logowania

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    level = Column(String) # INFO, ERROR, WARNING
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ScheduledAction(Base):
    __tablename__ = 'scheduled_actions'
    id = Column(Integer, primary_key=True)
    action_type = Column(String) # 'send_offer', 'rebump'
    payload = Column(Text) # JSON z danymi do akcji
    scheduled_time = Column(DateTime)
    is_completed = Column(Boolean, default=False)

engine = create_engine('sqlite:///smart_seller.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
