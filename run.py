from bot.bot import main
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

cfg_path = BASE_DIR/'config.ini'

main(cfg_path)
